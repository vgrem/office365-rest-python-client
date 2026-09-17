"""Report record IO — write record datasets in a chosen format.

Per-format, not CSV+JSON-coupled: :func:`write_dataset` picks a writer by name so
callers write whichever formats they need (``csv``/``json``/``ndjson``) by
looping, and adding a format is one registration.
"""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Callable, List, Optional, Sequence

RecordWriter = Callable[[List[dict], Path, Optional[Sequence[str]]], None]

_EXTENSIONS = {"csv": "csv", "json": "json", "ndjson": "ndjson"}


def _write_csv(records: list[dict], path: Path, columns: Optional[Sequence[str]] = None) -> None:
    from office365.runtime.converters.csv_writer import write_records

    with open(path, "w", newline="", encoding="utf-8") as f:
        write_records(records, f, list(columns) if columns else None)


def _write_json(records: list[dict], path: Path, columns: Optional[Sequence[str]] = None) -> None:
    from office365.runtime.converters.json_file import write_json

    with open(path, "w", encoding="utf-8") as f:
        write_json(records, f, indent=2)


def _write_ndjson(records: list[dict], path: Path, columns: Optional[Sequence[str]] = None) -> None:
    from office365.runtime.converters.ndjson import write_ndjson

    with open(path, "w", encoding="utf-8") as f:
        write_ndjson(records, f)


_WRITERS: dict[str, RecordWriter] = {"csv": _write_csv, "json": _write_json, "ndjson": _write_ndjson}


def write_dataset(
    records: list[dict],
    dir_: str | PathLike,
    stem: str,
    *,
    fmt: str = "csv",
    columns: Optional[Sequence[str]] = None,
) -> str:
    """Write ``records`` under ``dir_`` as ``stem.<ext>`` in ``fmt``; returns the path.

    Args:
        records: The record rows.
        dir_: Destination directory (created when missing).
        stem: File stem (without extension).
        fmt: One of ``csv``/``json``/``ndjson``.
        columns: Optional column order for CSV.
    """
    try:
        writer = _WRITERS[fmt]
    except KeyError:
        raise KeyError(f"Unknown report format {fmt!r}; known: {sorted(_WRITERS)}") from None
    path = Path(dir_) / f"{stem}.{_EXTENSIONS[fmt]}"
    path.parent.mkdir(parents=True, exist_ok=True)
    writer(records, path, columns)
    return str(path)


def write_formats(
    records: list[dict],
    dir_: str | PathLike,
    stem: str,
    *,
    formats: Sequence[str] = ("csv", "json"),
    columns: Optional[Sequence[str]] = None,
) -> list[str]:
    """Write the same records in each of ``formats``; returns the written paths."""
    return [write_dataset(records, dir_, stem, fmt=fmt, columns=columns) for fmt in formats]
