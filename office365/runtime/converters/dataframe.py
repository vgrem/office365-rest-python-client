"""pandas bridge — the optional-dependency boundary.

Every pandas-specific import lives here and is performed lazily, so the core
library never depends on pandas. Import this module or the thin
``ClientObjectCollection.to_dataframe``/``from_dataframe`` methods at your own
risk of requiring the ``[pandas]`` extra.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, cast

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


def series_kind(pd, series) -> str:
    """Categorize a pandas column dtype into a generic kind.

    Returns one of ``"boolean"``, ``"datetime"``, ``"number"``, ``"text"``.
    Kept in the pandas boundary so callers can map the generic kind onto their
    own schema (e.g. a SharePoint ``FieldType``) without importing pandas.

    Args:
        pd: The pandas module (e.g. from :func:`require_pandas`).
        series: A pandas Series (a DataFrame column).
    """
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_numeric_dtype(series):
        return "number"
    return "text"


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
