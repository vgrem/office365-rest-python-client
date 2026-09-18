"""pandas bridge — the optional-dependency boundary.

Every pandas-specific import lives here and is performed lazily, so the core
library never depends on pandas. Import this module or the thin
``ClientObjectCollection.to_dataframe``/``from_dataframe`` methods at your own
risk of requiring the ``[pandas]`` extra.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from os import PathLike
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterator, List, Optional, cast

from typing_extensions import Self

from office365.runtime.client_result import ClientResult

if TYPE_CHECKING:
    import pandas as pd


class DataFrameResult(ClientResult):
    """Result holder for ``to_dataframe()``.

    ``.value`` holds the pandas DataFrame after ``execute_query()``. Derives from
    the core ``ClientResult`` (which can now hold any value type) and narrows
    ``.value`` to ``pandas.DataFrame`` for type checkers — pandas stays optional.
    """

    @property
    def value(self) -> "pd.DataFrame":
        """The pandas DataFrame, populated after execute_query()."""
        return super().value

    def execute_query(self) -> Self:
        """Submit the deferred queries and return this result for chaining."""
        return cast(Self, super().execute_query())


def require_pandas():
    """Import pandas or raise an actionable error.

    Raises:
        ImportError: When pandas is not installed, pointing at the extra.
    """
    try:
        import pandas as pd  # type: ignore[import-not-found]
    except ImportError:
        raise ImportError("pip install office365-rest-python-client[pandas]") from None
    return pd


def write_dataframe(collection, target: "ClientResult") -> None:
    """Project a loaded collection into a pandas DataFrame and store it on ``target``.

    Args:
        collection: A loaded collection (items populated after execute_query()).
        target: A ``ClientResult`` whose ``.value`` holds the DataFrame afterwards.
    """
    from office365.runtime.converters.records import iter_records

    pd = require_pandas()
    records = iter_records(collection)
    df = pd.DataFrame.from_records(records) if records else pd.DataFrame()
    target.set_property("__value", df)


def read_dataframe(df) -> List[Dict[str, Any]]:
    """Convert a pandas DataFrame into plain dict records for import.

    NaN cells are dropped and keys kept as-is. Duck-typed: only
    ``df.to_dict("records")`` is required, so pandas itself is never imported.
    """
    return records_from_dataframe(df)


def dataframe_to_bytes(df, format: str = "csv", index: bool = False, **opts: Any) -> bytes:  # noqa: A002
    """Serialize a DataFrame to file bytes (``csv``/``xlsx``/``json``/``parquet``).

    CSV is written UTF-8 with a BOM (``utf-8-sig``) so Excel keeps the columns.
    """
    import io

    if format in ("xlsx", "excel"):
        buffer = io.BytesIO()
        df.to_excel(buffer, index=index, **opts)
        return buffer.getvalue()
    if format == "json":
        return df.to_json(**opts).encode("utf-8")
    if format in ("parquet", "orc", "feather"):
        buffer = io.BytesIO()
        writer = {"parquet": df.to_parquet, "orc": df.to_orc, "feather": df.to_feather}[format]
        writer(buffer, **opts)
        return buffer.getvalue()
    return df.to_csv(index=index, **opts).encode("utf-8-sig")


def dataframe_from_bytes(content: bytes, format: str = "csv", **opts: Any) -> "pd.DataFrame":  # noqa: A002
    """Parse in-memory file bytes into a DataFrame (``csv``/``xlsx``/``json``/``parquet``)."""
    import io

    pd = require_pandas()
    buffer = io.BytesIO(content)
    if format in ("xlsx", "excel"):
        return pd.read_excel(buffer, **opts)
    if format == "json":
        return pd.read_json(buffer, **opts)
    if format in ("parquet", "orc", "feather"):
        reader = {"parquet": pd.read_parquet, "orc": pd.read_orc, "feather": pd.read_feather}[format]
        return reader(buffer, **opts)
    return pd.read_csv(buffer, **opts)


def series_kind(pd, series) -> str:
    """Categorize a pandas column dtype into a generic kind.

    Returns one of ``"boolean"``, ``"datetime"``, ``"number"``, ``"text"``.
    Kept in the pandas boundary so callers can map the generic kind onto their
    own schema (e.g. a SharePoint ``FieldType``) without importing pandas.

    Nullable dtypes are handled; complex and timedelta map to ``"text"`` (no
    SharePoint equivalent), and an object column holding only ``datetime``/``date``
    values is treated as ``"datetime"``.

    Args:
        pd: The pandas module (e.g. from :func:`require_pandas`).
        series: A pandas Series (a DataFrame column).
    """
    dtype = series.dtype
    if pd.api.types.is_bool_dtype(dtype):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "datetime"
    if pd.api.types.is_complex_dtype(dtype):
        return "text"
    if pd.api.types.is_numeric_dtype(dtype):
        return "number"
    if pd.api.types.is_object_dtype(dtype) and _holds_datetimes(series):
        return "datetime"
    return "text"


def _holds_datetimes(series) -> bool:
    """Whether an object-dtype column holds only ``datetime``/``date`` values."""
    non_null = series.dropna()
    if non_null.empty:
        return False
    return all(isinstance(value, (datetime, date)) for value in non_null.head(100))


def records_from_dataframe(
    df,
    key_fn: Optional[Callable[[str], str]] = None,
) -> List[Dict[str, Any]]:
    """Convert a DataFrame into importable dict records.

    Cells that are NaN are omitted (otherwise ``json.dumps`` would emit invalid
    ``NaN`` in create payloads). ``key_fn`` optionally renames record keys —
    e.g. to sanitize column names into field internal names.

    Args:
        df: A pandas DataFrame (duck-typed: only ``to_dict`` is required).
        key_fn: Optional column-name mapping applied to each record key.

    Returns:
        A list of dict records (one per row).
    """
    records: List[Dict[str, Any]] = []
    for raw in df.to_dict("records"):
        record: Dict[str, Any] = {}
        for key, value in raw.items():
            if isinstance(value, float) and math.isnan(value):
                continue
            record[key_fn(key) if key_fn is not None else key] = value
        records.append(record)
    return records


def dataframe_chunks(source: Any, chunksize: int) -> tuple[Iterator[Any], Optional[int]]:
    """Split a DataFrame/CSV source into chunks, with the total when known.

    Accepts a ``DataFrame`` (sliced into ``chunksize``-row slices), a CSV
    path/URL/file (read with ``pandas.read_csv(chunksize=)``), a pandas chunk
    reader (``pd.read_csv(..., chunksize=)``, used as-is), or any iterable of
    chunks (used as-is). Returns ``(chunks, total)`` — ``total`` is ``None`` when
    it can't be known upfront (a CSV stream or an opaque iterable).

    Args:
        source: A DataFrame, a CSV path/URL/file, or an iterable of chunks.
        chunksize: Rows per chunk for a DataFrame or CSV source.
    """
    if hasattr(source, "iloc"):  # a pandas DataFrame — slice it (bounded queue)
        total = len(source)
        return (source.iloc[start : start + chunksize] for start in range(0, total, chunksize)), total
    if hasattr(source, "get_chunk"):  # a pandas TextFileReader (already chunked) — iterate
        return iter(source), None
    if isinstance(source, (str, PathLike)) or hasattr(source, "read"):
        pd = require_pandas()
        return pd.read_csv(source, chunksize=chunksize), None
    return iter(source), None
