"""Shared helpers for the migration toolkit (progress, CSV/JSON, timestamps).

Keeps the small, repeated idioms (progress emission, record export, ISO-8601
timestamps) in one place instead of inlining them in every adapter/runner.
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def emit_progress(progress, *, done: int, total: int | None = None, stage: str, items=None) -> None:
    """Invoke a progress hook (if any) with a ``Progress`` snapshot.

    Centralizes the ``if callable(progress): Progress(...)`` idiom used across
    the toolkit.
    """
    if callable(progress):
        from office365.runtime.operations import Progress

        progress(Progress(done=done, total=total, stage=stage, items=items))


def write_csv_json(dir_: str | Path, stem: str, records: list[dict], columns: list[str] | None = None) -> list[str]:
    """Write records as both CSV and JSON under ``dir_``; returns the file paths."""
    os.makedirs(dir_, exist_ok=True)
    columns = list(columns) if columns else (list(records[0]) if records else [])

    csv_path = os.path.join(str(dir_), f"{stem}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, restval="n/a")
        writer.writeheader()
        writer.writerows(records)

    json_path = os.path.join(str(dir_), f"{stem}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    return [csv_path, json_path]


def utc_now_iso() -> str:
    """Current UTC time as an ISO-8601 string (second precision)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def iso(value) -> str:
    """ISO-8601 string for a datetime (second precision); ``""`` for ``None``."""
    if value is None:
        return ""
    return value.isoformat(timespec="seconds")


def iso_or_none(value) -> str | None:
    """ISO-8601 string for a datetime, or ``None`` when unset/absent.

    Treats ``datetime.min`` (the "not loaded" sentinel used by some SharePoint
    properties) as unset.
    """
    if value is None or value == datetime.min:
        return None
    return value.isoformat(timespec="seconds") if hasattr(value, "isoformat") else (str(value) or None)


def record_to_json(payload: object) -> str:
    """Serialize a record to the canonical JSON text used when persisting it.

    SharePoint property values are often entity/datetime objects, so a str
    fallback keeps the payload JSON-safe. Source/target checksums both use this
    form, so content verification compares identical text.
    """
    return json.dumps(payload, indent=2, default=str)
