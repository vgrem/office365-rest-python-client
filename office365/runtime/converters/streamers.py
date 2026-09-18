"""Incremental (paged) writers for the streaming exporter.

Only row-appendable formats support paging (CSV/TSV/NDJSON/JSON); the exporter
falls back to a whole-collection write otherwise. Each streamer is a small
object with ``write(records)`` and ``close()``.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class RecordStreamWriter(Protocol):
    """Append-only writer used by ``export_to(..., page_size=...)``."""

    def write(self, records: List[Dict[str, Any]]) -> None:
        """Append a page of records."""
        ...

    def close(self) -> None:
        """Finalize and release the target."""
        ...


class CsvStreamWriter:
    """Append CSV/TSV rows, writing the header on the first page."""

    def __init__(self, target: Any, delimiter: str = ",") -> None:
        from office365.runtime.converters.csv_writer import write_records, write_rows
        from office365.runtime.converters.streams import open_text

        self._write_records = write_records
        self._write_rows = write_rows
        self._delimiter = delimiter
        self._columns: Optional[List[str]] = None
        self._ctx = open_text(target, "w")
        self._file = self._ctx.__enter__()

    def write(self, records: List[Dict[str, Any]]) -> None:
        if not records:
            return
        if self._columns is None:
            self._columns = list(dict.fromkeys(key for record in records for key in record))
            self._write_records(records, self._file, columns=self._columns, delimiter=self._delimiter)
        else:
            self._write_rows(records, self._file, self._columns, self._delimiter)

    def close(self) -> None:
        self._ctx.__exit__(None, None, None)


class NdjsonStreamWriter:
    """Append NDJSON lines."""

    def __init__(self, target: Any) -> None:
        from office365.runtime.converters.ndjson import write_ndjson
        from office365.runtime.converters.streams import open_text

        self._write_ndjson = write_ndjson
        self._ctx = open_text(target, "w")
        self._file = self._ctx.__enter__()

    def write(self, records: List[Dict[str, Any]]) -> None:
        self._write_ndjson(records, self._file)

    def close(self) -> None:
        self._ctx.__exit__(None, None, None)


class JsonArrayStreamWriter:
    """Append a single JSON array across pages."""

    def __init__(self, target: Any) -> None:
        from office365.runtime.converters.streams import open_text

        self._ctx = open_text(target, "w")
        self._file = self._ctx.__enter__()
        self._file.write("[")
        self._first = True

    def write(self, records: List[Dict[str, Any]]) -> None:
        for record in records:
            if not self._first:
                self._file.write(",")
            json.dump(record, self._file, default=str)
            self._first = False

    def close(self) -> None:
        self._file.write("]")
        self._ctx.__exit__(None, None, None)


_STREAMERS: Dict[str, Callable[..., RecordStreamWriter]] = {
    "csv": lambda target, **opts: CsvStreamWriter(target, opts.get("delimiter", ",")),
    "tsv": lambda target, **opts: CsvStreamWriter(target, "\t"),
    "ndjson": lambda target, **opts: NdjsonStreamWriter(target),
    "json": lambda target, **opts: JsonArrayStreamWriter(target),
}


def streamer_for(name: str) -> Optional[Callable[..., RecordStreamWriter]]:
    """The incremental writer factory for ``name``, or ``None`` (not appendable)."""
    return _STREAMERS.get(name)
