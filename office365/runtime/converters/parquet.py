"""Parquet/ORC/Feather reader/writer via pyarrow — the optional-dependency boundary.

Every function imports pyarrow lazily, so the core library never depends on it
(``pip install office365-rest-python-client[parquet]``). Sources/targets accept a
path or an open binary stream.
"""

from __future__ import annotations

from typing import Any, Dict, List


def require_pyarrow():
    """Import pyarrow or raise an actionable error."""
    try:
        import pyarrow  # type: ignore[import-not-found]
    except ImportError:
        raise ImportError("pip install office365-rest-python-client[parquet]") from None
    return pyarrow


def _read(source: Any, reader: str) -> List[Dict[str, Any]]:
    require_pyarrow()
    from office365.runtime.converters.streams import open_binary

    module = __import__(f"pyarrow.{reader}", fromlist=["read_table"])
    with open_binary(source, "rb") as f:
        return module.read_table(f).to_pylist()


def _write(records: List[Dict[str, Any]], target: Any, writer: str) -> None:
    import pyarrow as pa  # type: ignore[import-not-found]

    require_pyarrow()
    from office365.runtime.converters.streams import open_binary

    module = __import__(f"pyarrow.{writer}", fromlist=["write_table"])
    table = pa.Table.from_pylist(records)
    with open_binary(target, "wb") as f:
        if writer == "feather":
            module.write_feather(table, f)
        else:
            module.write_table(table, f)


def read_parquet(source: Any) -> List[Dict[str, Any]]:
    return _read(source, "parquet")


def write_parquet(records: List[Dict[str, Any]], target: Any) -> None:
    _write(records, target, "parquet")


def read_orc(source: Any) -> List[Dict[str, Any]]:
    return _read(source, "orc")


def write_orc(records: List[Dict[str, Any]], target: Any) -> None:
    _write(records, target, "orc")


def read_feather(source: Any) -> List[Dict[str, Any]]:
    return _read(source, "feather")


def write_feather(records: List[Dict[str, Any]], target: Any) -> None:
    _write(records, target, "feather")
