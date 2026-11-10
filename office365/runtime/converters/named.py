"""The named converters: every spelling a per-column spec may use, and its resolver.

A converter answers exactly one cell. It receives what the reader produced -- a CSV
cell is usually text, but pandas hands back an ``int`` for a numeric column -- and
returns the value the destination stores. Every built-in tolerates a value that is
already typed (``try_int(30) -> 30``, ``parse_datetime(datetime(...)) -> datetime``)
because a converter can meet both a raw cell and the output of an earlier pass.

Four spellings resolve to one single-argument callable (:func:`converter_for`):

    {"startDateTime": "Edm.DateTimeOffset"}   # a name the wire already uses
    {"accountEnabled": bool}                  # the Python type the model declares
    {"Tags": FieldType.MultiChoice}           # a SharePoint field type
    {"legacy_room": my_parser}                # a column only you know about

A column you do not list is deserialized from the property type the model declares
(applied at entity construction: ``set_property`` -> ``deserialize_value``), and a
column the type does not declare is dropped unless the destination accepts arbitrary
columns -- a SharePoint list item does, a typed Graph entity does not.
"""

from __future__ import annotations

from enum import Enum
from functools import partial
from typing import Any, Callable, Dict

from office365.runtime.converters.scalars import (
    deserialize_enum,
    parse_bool,
    parse_date,
    parse_datetime,
    parse_decimal,
    parse_duration,
    parse_uuid,
    try_float,
    try_int,
)
from office365.runtime.odata.edm import PRIMITIVES, parser_for, primitive_type_for

#: A converter takes one raw cell and returns the value the destination stores.
Converter = Callable[[Any], Any]

#: One column's converter: a callable, a Python type, a type name, or a SharePoint ``FieldType``.
ConverterSpec = Any

#: The built-ins by name. Every EDM spelling is derived from the one primitive table, so a
#: Python type cannot be spelled two ways in two places; the rest are the Python spellings a
#: column may use. Names are matched case-insensitively on the last dotted segment, so
#: ``"Edm.DateTimeOffset"`` and ``"datetimeoffset"`` are the same entry.
CONVERTERS: Dict[str, Converter] = {
    edm.rsplit(".", 1)[-1].lower(): converter
    for converter, names in PRIMITIVES.values()
    for edm in names
    if converter is not None
}
CONVERTERS.update(
    {
        "str": str,
        "string": str,
        "int": try_int,
        "integer": try_int,
        "bool": parse_bool,
        "float": try_float,
        "number": try_float,
        "decimal": parse_decimal,
        "datetime": parse_datetime,
        "date": parse_date,
        "timespan": parse_duration,
        "uuid": parse_uuid,
    }
)


def converter_for(spec: ConverterSpec) -> Converter:
    """Resolve one per-column spec to the callable that applies it.

    A callable is returned unchanged -- it is the primitive every other spelling
    resolves to, so the import path only ever calls a plain one-argument callable.
    An enum resolves to the deserializer the value layer uses, so a member the
    snapshot does not list is kept as sent rather than raised on. A ``FieldType``
    resolves to the SharePoint payload conversion for that field type; a name that is
    neither a built-in nor an EDM primitive raises ``ValueError``, so a typo cannot
    silently mean "no conversion".
    """
    if isinstance(spec, str):
        return _named(spec)
    if isinstance(spec, type):
        if issubclass(spec, Enum):
            return partial(deserialize_enum, spec)
        return parser_for(spec) or spec
    if callable(spec):
        return spec
    if _is_field_type(spec):
        from office365.sharepoint.fields.coercion import coerce_field_value

        return partial(coerce_field_value, spec)
    raise TypeError(f"a converter expects a callable, a type, a type name or a FieldType, got {spec!r}")


def _named(name: str) -> Converter:
    """Resolve a type name: a built-in spelling first, then an EDM primitive name."""
    spelled = name.strip()
    converter = CONVERTERS.get(spelled.rsplit(".", 1)[-1].lower())
    if converter is not None:
        return converter
    python_type = primitive_type_for(spelled)
    if python_type is not None:
        raise ValueError(
            f"{name!r} names {python_type.__name__}, which has no built-in converter; pass a callable for it"
        )
    raise ValueError(f"Unknown converter {name!r}; known names: {', '.join(sorted(CONVERTERS))}")


def _is_field_type(value: Any) -> bool:
    """Whether ``value`` is a SharePoint ``FieldType`` member (imported lazily)."""
    from office365.sharepoint.fields.type import FieldType

    return isinstance(value, FieldType)
