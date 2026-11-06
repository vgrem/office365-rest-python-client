"""CSV/records parsing for the collection import pipeline.

CSV files and JSON/Excel/pandas records are normalized into plain ``dict``
records (via :func:`coerce_records`) which the collection ``from_*`` methods
turn into entities via the shared conversion core (``create_typed_object`` ->
``set_property`` -> ``coerce_value``/``declared_type``).
"""

from __future__ import annotations

import csv
import warnings
from typing import IO, Any, get_origin

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.converters.coercion import Coercer, ConverterSpec, converter_for
from office365.runtime.converters.value import declared_type

_LIST_SEPARATOR = "; "


def read_csv_records(file: IO[str], delimiter: str = ",") -> list[dict]:
    """Parse CSV rows into plain dict records (empty cells dropped).

    Type-aware normalization (dotted keys, ``"; "`` collection splitting,
    unknown-column skipping) is applied later by :func:`coerce_records` when the
    records are imported.
    """
    reader = csv.DictReader(file, delimiter=delimiter)
    if reader.fieldnames is None:
        return []
    return [{k: v for k, v in row.items() if v not in ("", None)} for row in reader]


def coerce_records(
    item_type: type,
    records: list[dict],
    *,
    coerce: "dict[str, ConverterSpec] | None" = None,
    allow_unknown: bool = False,
) -> list[dict]:
    """Normalize plain dict records to the entity's declared property types.

    Dotted keys (``a/b/c``) are re-nested into dicts; ``"; "``-joined strings are
    split for collection-typed fields; non-importable keys (``@*``, ``id``) and
    ``None`` cells are dropped; columns mapping to no known property are skipped
    with a warning. Pass ``allow_unknown=True`` for schema-flexible targets whose
    fields are only known at runtime (SharePoint list items). Shared by every
    import format.

    ``coerce`` maps a *record key* (dotted keys included) to one value converter, as a
    callable, a Python type, a type name or a ``FieldType`` -- see
    :func:`~office365.runtime.converters.coercion.converter_for`. A converter wins over
    the column's declared type; a converter naming a column the type does not declare
    raises, so a typo cannot silently drop the column it meant to type.
    """
    converters = resolve_converters(item_type, coerce, allow_unknown)
    coerced: list[dict[str, Any]] = []
    for record in records:
        item: dict[str, Any] = {}
        for key, raw in record.items():
            if not _is_importable(key):
                continue
            if raw is None:
                continue
            converter = converters.get(key)
            if "/" in key:
                nav = key.split("/", 1)[0]
                if declared_type(item_type, nav) is None and not allow_unknown:
                    warnings.warn(f"Skipping unknown column '{key}'", stacklevel=2)
                    continue
                _set_nested(item, key, converter(raw) if converter is not None else raw)
                continue
            declared = declared_type(item_type, key)
            if declared is None and not allow_unknown:
                warnings.warn(f"Skipping unknown column '{key}'", stacklevel=2)
                continue
            if converter is not None:
                item[key] = converter(raw)
            elif isinstance(raw, str) and declared is not None and _is_collection(declared):
                item[key] = raw.split(_LIST_SEPARATOR)
            else:
                item[key] = raw
        coerced.append(item)
    return coerced


def apply_converters(records: list[dict], converters: dict[str, "Coercer"]) -> list[dict]:
    """Apply resolved converters cell by cell, leaving every other key untouched.

    No filtering and no declared-type work: this is the user's ``coerce`` layer alone,
    so it can run before a keyed import where the key columns need not be declared on
    the model. ``None`` cells are skipped (an empty cell states nothing).
    """
    if not converters:
        return records
    return [
        {
            key: (converters[key](value) if key in converters and value is not None else value)
            for key, value in record.items()
        }
        for record in records
    ]


def resolve_converters(
    item_type: type,
    coerce: "dict[str, ConverterSpec] | None",
    allow_unknown: bool,
) -> dict[str, "Coercer"]:
    """Resolve every ``coerce`` spec once, and reject keys the type cannot store."""
    if not coerce:
        return {}
    resolved: dict[str, Coercer] = {}
    for column, spec in coerce.items():
        if declared_type(item_type, column.split("/", 1)[0]) is None and not allow_unknown:
            raise ValueError(
                f"coerce has no column {column!r} in {item_type.__name__}; "
                "check the destination key, or pass allow_unknown=True for a target that accepts arbitrary columns"
            )
        resolved[column] = converter_for(spec)
    return resolved


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
