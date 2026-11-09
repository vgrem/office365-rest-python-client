"""Cell-level coercion: the named built-ins, and the resolver that turns a spec into one callable.

A converter answers exactly one cell. It receives what the reader produced -- a CSV
cell is usually text, but pandas hands back an ``int`` for a numeric column -- and
returns the value the destination stores. Every built-in tolerates a value that is
already typed (``try_int(30) -> 30``, ``parse_datetime(datetime(...)) -> datetime``)
because a converter can meet both a raw cell and the output of an earlier pass.

``coerce=`` on an import maps a *destination* column to one of four spellings, and all
four resolve to the same single-argument callable here:

    {"startDateTime": "Edm.DateTimeOffset"}   # a name the wire already uses
    {"accountEnabled": bool}                  # the Python type the model declares
    {"Tags": FieldType.MultiChoice}           # a SharePoint field type
    {"legacy_room": my_parser}                # a column only you know about

Columns you do not list are typed from the property type the model declares (applied at
entity construction: ``set_property`` -> ``deserialize_value``), and a column the type does
not declare is dropped unless the destination accepts arbitrary columns -- a SharePoint
list item does, a typed Graph entity does not.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from functools import partial
from typing import Any, Callable, Dict
from uuid import UUID

from office365.runtime.converters.scalars import (
    parse_bool,
    parse_date,
    parse_datetime,
    parse_decimal,
    parse_duration,
    parse_uuid,
    try_float,
    try_int,
)
from office365.runtime.odata.edm import primitive_type_for

#: A converter takes one raw cell and returns the value the destination stores.
Coercer = Callable[[Any], Any]

#: One column's coercion: a callable, a Python type, a type name, or a SharePoint ``FieldType``.
ConverterSpec = Any

#: The built-ins by name -- the discoverable half of the registry. Names are matched
#: case-insensitively on the last dotted segment, so ``"Edm.DateTimeOffset"`` and
#: ``"datetimeoffset"`` are the same entry.
CONVERTERS: Dict[str, Coercer] = {
    "str": str,
    "string": str,
    "bool": parse_bool,
    "boolean": parse_bool,
    "int": try_int,
    "integer": try_int,
    "float": try_float,
    "double": try_float,
    "number": try_float,
    "decimal": parse_decimal,
    "datetime": parse_datetime,
    "datetimeoffset": parse_datetime,
    "date": parse_date,
    "duration": parse_duration,
    "timespan": parse_duration,
    "guid": parse_uuid,
    "uuid": parse_uuid,
}

#: The same built-ins keyed by the Python type they produce, so ``coerce={"due": date}``
#: and ``coerce={"due": "Edm.Date"}`` agree. A type that is not listed is used as its own
#: constructor (``Path``, an enum, a ``ClientValue`` class), which is the general arm.
_TYPE_CONVERTERS: Dict[type, Coercer] = {
    str: str,
    bool: parse_bool,
    int: try_int,
    float: try_float,
    Decimal: parse_decimal,
    datetime: parse_datetime,
    date: parse_date,
    timedelta: parse_duration,
    UUID: parse_uuid,
}


def converter_for(spec: ConverterSpec) -> Coercer:
    """Resolve one ``coerce`` value to the callable that applies it.

    A callable is returned unchanged -- it is the primitive every other spelling
    resolves to, so the import path only ever calls a plain one-argument callable.
    A ``FieldType`` resolves to the SharePoint payload coercion for that field type;
    a name that is neither a built-in nor an EDM primitive raises ``ValueError``, so a
    typo cannot silently mean "no coercion".
    """
    if isinstance(spec, str):
        return _named(spec)
    if isinstance(spec, type):
        return _TYPE_CONVERTERS.get(spec, spec)
    if callable(spec):
        return spec
    if _is_field_type(spec):
        from office365.sharepoint.fields.coercion import coerce_field_value

        return partial(coerce_field_value, spec)
    raise TypeError(f"coerce expects a callable, a type, a type name or a FieldType, got {spec!r}")


def _named(name: str) -> Coercer:
    """Resolve a type name: a built-in spelling first, then an EDM primitive name."""
    key = name.strip()
    builtin = CONVERTERS.get(key.rsplit(".", 1)[-1].lower())
    if builtin is not None:
        return builtin
    python_type = primitive_type_for(key)
    if python_type in _TYPE_CONVERTERS:
        return _TYPE_CONVERTERS[python_type]
    if python_type is not None:
        raise ValueError(
            f"{name!r} names {python_type.__name__}, which has no built-in converter; pass a callable for it"
        )
    known = ", ".join(sorted(CONVERTERS))
    raise ValueError(f"Unknown converter {name!r}; known names: {known}")


def _is_field_type(value: Any) -> bool:
    """Whether ``value`` is a SharePoint ``FieldType`` member (imported lazily)."""
    from office365.sharepoint.fields.type import FieldType

    return isinstance(value, FieldType)
