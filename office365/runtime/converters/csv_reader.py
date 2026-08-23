"""CSV/records parsing for the collection import pipeline.

CSV files and JSON records are normalized into plain ``dict`` records which the
collection ``from_csv``/``from_json`` methods turn into entities via the shared
conversion core (``create_typed_object`` -> ``set_property`` ->
``deserialize_value``/``declared_type``).
"""

from __future__ import annotations

import csv
import warnings
from typing import IO, Any, get_origin

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.value import declared_type

_LIST_SEPARATOR = "; "


def read_csv_records(item_type: type, file: IO[str], delimiter: str = ",") -> list[dict]:
    """Parse CSV rows into records, using the entity's declared property types.

    Dotted headers (``passwordProfile/password``) are re-nested into dicts.
    ``"; "``-joined cells are split for collection-typed fields. Columns that map
    to no known property are skipped with a warning.
    """
    reader = csv.DictReader(file, delimiter=delimiter)
    if reader.fieldnames is None:
        return []
    records = []
    for row in reader:
        record: dict[str, Any] = {}
        for key in reader.fieldnames:
            if not _is_importable(key):
                continue
            raw = row.get(key, "")
            if raw == "" or raw is None:
                continue
            if "/" in key:
                nav = key.split("/", 1)[0]
                if declared_type(item_type, nav) is None:
                    warnings.warn(f"Skipping unknown CSV column '{key}'", stacklevel=2)
                    continue
                _set_nested(record, key, raw)
                continue
            declared = declared_type(item_type, key)
            if declared is None:
                warnings.warn(f"Skipping unknown CSV column '{key}'", stacklevel=2)
                continue
            if isinstance(raw, str) and _is_collection(declared):
                record[key] = raw.split(_LIST_SEPARATOR)
            else:
                record[key] = raw
        records.append(record)
    return records


def clean_records(records: list[dict]) -> list[dict]:
    """Strip non-importable cells (``@*``, ``id``, ``None``) from JSON records."""
    return [{k: v for k, v in record.items() if _is_importable(k) and v is not None} for record in records]


def _is_importable(key: str) -> bool:
    """Decide whether a record key should be imported at all."""
    return not key.startswith("@") and key != "id"


def _is_collection(target_type: Any) -> bool:
    """Decide whether a declared type represents a list/collection field."""
    return get_origin(target_type) in (list, tuple, set) or (
        isinstance(target_type, type) and issubclass(target_type, ClientValueCollection)
    )


def _set_nested(record: dict[str, Any], key: str, value: Any) -> None:
    """Re-nest a dotted header (``a/b/c``) into nested dicts."""
    parts = key.split("/")
    node = record
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = value
