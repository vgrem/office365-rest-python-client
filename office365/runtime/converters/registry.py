"""Format registry — maps a format name to its record reader/writer.

Keeps the import/export surface of :class:`~office365.runtime.record_collection.RecordCollection`
data-driven: adding a format is a registration, not a new method. Readers turn a
source into plain dict records; writers persist a collection's records to a
target. Both import their (optional) dependency lazily, so registering a format
never pulls in pandas/openpyxl.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, List

if TYPE_CHECKING:
    from office365.runtime.client_object_collection import ClientObjectCollection

RecordReader = Callable[..., List[dict]]
RecordWriter = Callable[..., None]

_READERS: Dict[str, RecordReader] = {}
_WRITERS: Dict[str, RecordWriter] = {}


def register(name: str, *, reader: RecordReader, writer: RecordWriter) -> None:
    """Register (or replace) a format's reader and writer."""
    _READERS[name] = reader
    _WRITERS[name] = writer


def reader_for(name: str) -> RecordReader:
    """The reader for a format, or a ``KeyError`` listing the known formats."""
    try:
        return _READERS[name]
    except KeyError:
        raise KeyError(f"Unknown import format {name!r}; known: {sorted(_READERS)}") from None


def writer_for(name: str) -> RecordWriter:
    """The writer for a format, or a ``KeyError`` listing the known formats."""
    try:
        return _WRITERS[name]
    except KeyError:
        raise KeyError(f"Unknown export format {name!r}; known: {sorted(_WRITERS)}") from None


def formats() -> List[str]:
    """The registered format names."""
    return sorted(set(_READERS) | set(_WRITERS))


# ── Built-in formats (lazy imports) ──────────────────────────────


def _read_csv(file: Any, **opts: Any) -> List[dict]:
    from office365.runtime.converters.csv_reader import read_csv_records

    return read_csv_records(file, opts.get("delimiter", ","))


def _write_csv(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.csv_writer import write_csv

    write_csv(collection, target)


def _read_ndjson(file: Any, **opts: Any) -> List[dict]:
    from office365.runtime.converters.ndjson import read_ndjson

    return read_ndjson(file)


def _write_ndjson(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.ndjson import write_ndjson
    from office365.runtime.converters.records import iter_records

    write_ndjson(iter_records(collection), target)


def _read_json_file(file: Any, **opts: Any) -> List[dict]:
    from office365.runtime.converters.json_file import read_json

    return read_json(file)


def _write_json_file(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.json_file import write_json
    from office365.runtime.converters.records import iter_records

    write_json(iter_records(collection), target)


def _read_excel(path: Any, **opts: Any) -> List[dict]:
    from office365.runtime.converters.excel import read_excel

    return read_excel(path)


def _write_excel(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.excel import write_excel
    from office365.runtime.converters.records import iter_records

    write_excel(iter_records(collection), target)


def _read_dataframe(df: Any, **opts: Any) -> List[dict]:
    from office365.runtime.converters.dataframe import read_dataframe

    return read_dataframe(df)


def _write_dataframe(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.dataframe import write_dataframe

    write_dataframe(collection, target)


register("csv", reader=_read_csv, writer=_write_csv)
register("ndjson", reader=_read_ndjson, writer=_write_ndjson)
register("json", reader=_read_json_file, writer=_write_json_file)
register("json_file", reader=_read_json_file, writer=_write_json_file)  # deprecated alias
register("excel", reader=_read_excel, writer=_write_excel)
register("dataframe", reader=_read_dataframe, writer=_write_dataframe)
