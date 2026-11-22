"""Format registry — maps a format name to its record reader/writer.

Keeps the import/export surface of :class:`~office365.runtime.record_collection.RecordCollection`
data-driven: adding a format is a registration, not a new method. Readers turn a
source into :data:`~office365.runtime.converters.records.Record` rows; writers persist
a collection's records to a target. Both import their (optional) dependency lazily,
so registering a format never pulls in pandas/openpyxl.

``source``, ``target`` and ``**opts`` are ``Any`` here for the reason the table exists:
it is open.  A reader takes a path, a URL, an open file, a DataFrame or a buffer and a
writer the same, each of which the *format* decides; ``opts`` are that format's own
keyword arguments, passed through untouched.  A union in this signature would refuse
the next format someone registers -- which is exactly what registering is for.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from office365.runtime.client_object_collection import ClientObjectCollection
    from office365.runtime.converters.records import Record

RecordReader = Callable[..., list["Record"]]
RecordWriter = Callable[..., None]

_READERS: dict[str, RecordReader] = {}
_WRITERS: dict[str, RecordWriter] = {}


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


def formats() -> list[str]:
    """The registered format names."""
    return sorted(set(_READERS) | set(_WRITERS))


# ── Built-in formats (lazy imports) ──────────────────────────────


def _records(collection: "ClientObjectCollection", rows_from: str | None) -> list["Record"]:
    """A collection's records, in the shape the format's writer takes.

    One row per item, or one row per child when the caller named ``rows_from`` -- the
    reading side of the same option.  Every built-in format below asks for its rows this
    way, so "what is a row" is answered once instead of once per writer.
    """
    from office365.runtime.converters.records import iter_records

    return iter_records(collection, rows_from=rows_from)


def _read_csv(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.csv_reader import read_csv_records
    from office365.runtime.converters.streams import open_text

    with open_text(source, "r") as f:
        return read_csv_records(f, opts.get("delimiter", ","))


def _write_csv(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.csv_writer import write_records
    from office365.runtime.converters.streams import open_text

    with open_text(target, "w") as f:
        write_records(_records(collection, opts.get("rows_from")), f, delimiter=opts.get("delimiter", ","))


def _read_tsv(source: Any, **opts: Any) -> list[Record]:
    return _read_csv(source, delimiter="\t", **opts)


def _write_tsv(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    _write_csv(collection, target, delimiter="\t", **opts)


def _read_ndjson(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.ndjson import read_ndjson
    from office365.runtime.converters.streams import open_text

    with open_text(source, "r") as f:
        return read_ndjson(f)


def _write_ndjson(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.ndjson import write_ndjson
    from office365.runtime.converters.streams import open_text

    with open_text(target, "w") as f:
        write_ndjson(_records(collection, opts.get("rows_from")), f)


def _read_json_file(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.json_file import read_json
    from office365.runtime.converters.streams import open_text

    with open_text(source, "r") as f:
        return read_json(f)


def _write_json_file(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.json_file import write_json
    from office365.runtime.converters.streams import open_text

    with open_text(target, "w") as f:
        write_json(_records(collection, opts.get("rows_from")), f, indent=opts.get("indent"))


def _read_excel(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.excel import read_excel

    return read_excel(source)


def _write_excel(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.excel import write_excel

    write_excel(_records(collection, opts.get("rows_from")), target)


def _read_dataframe(df: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.dataframe import read_dataframe

    return read_dataframe(df)


def _write_dataframe(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.dataframe import write_dataframe

    write_dataframe(collection, target)


def _read_parquet(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.parquet import read_parquet

    return read_parquet(source)


def _write_parquet(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.parquet import write_parquet

    write_parquet(_records(collection, opts.get("rows_from")), target)


def _read_orc(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.parquet import read_orc

    return read_orc(source)


def _write_orc(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.parquet import write_orc

    write_orc(_records(collection, opts.get("rows_from")), target)


def _read_feather(source: Any, **opts: Any) -> list[Record]:
    from office365.runtime.converters.parquet import read_feather

    return read_feather(source)


def _write_feather(collection: "ClientObjectCollection", target: Any, **opts: Any) -> None:
    from office365.runtime.converters.parquet import write_feather

    write_feather(_records(collection, opts.get("rows_from")), target)


register("csv", reader=_read_csv, writer=_write_csv)
register("tsv", reader=_read_tsv, writer=_write_tsv)
register("json", reader=_read_json_file, writer=_write_json_file)
register("json_file", reader=_read_json_file, writer=_write_json_file)  # deprecated alias
register("ndjson", reader=_read_ndjson, writer=_write_ndjson)
register("excel", reader=_read_excel, writer=_write_excel)
register("dataframe", reader=_read_dataframe, writer=_write_dataframe)
register("parquet", reader=_read_parquet, writer=_write_parquet)
register("orc", reader=_read_orc, writer=_write_orc)
register("feather", reader=_read_feather, writer=_write_feather)
