"""The EDM grammar: primitive names, and the name a Python class declares.

OData type *references* are strings (``Collection(microsoft.graph.User)``) and are
CSDL syntax: only the generator parses them, once, into
:class:`generator.odata.type_system.TypeRef`. The runtime asks the inverse question —
"given this Python class, what does OData call it?" — which is a declaration read,
not string surgery::

    edm_type_name(str)  # "Edm.String"
    edm_type_name(Event)  # "microsoft.graph.Event"
    collection_type_name(Event)  # "Collection(microsoft.graph.Event)"

A model declares its name once, as the ``entity_type_name`` property generated into
every class. Reading that name off a *class* is not possible (a property needs an
instance), so a class that must be asked without one also declares the
``_odata_type_name`` class fact, and resolving a name then never builds the model:
a ``ClientObject`` subclass cannot be constructed without a context, and a lookup
that *needs* one is a lookup with a hidden side effect. Classes declaring neither
fall back to one throwaway instance (cached per class).
"""

from __future__ import annotations

import datetime
import uuid
from decimal import Decimal
from functools import cache
from typing import Any, Callable, Optional, Type

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

#: One row per Python type the wire has: the cell parser the conversion layer uses for it
#: (``None`` for a type a cell is never read back as) and every EDM name it answers to.
#: The name order is the spelling order: the first name is the one the runtime writes.
PRIMITIVES: dict[type, tuple[Optional[Callable[[Any], Any]], tuple[str, ...]]] = {
    bool: (parse_bool, ("Edm.Boolean",)),
    int: (try_int, ("Edm.Int32", "Edm.Int64", "Edm.Int16", "Edm.Byte", "Edm.SByte")),
    str: (None, ("Edm.String",)),
    uuid.UUID: (parse_uuid, ("Edm.Guid",)),
    float: (try_float, ("Edm.Single", "Edm.Double")),
    Decimal: (parse_decimal, ("Edm.Decimal",)),
    bytes: (None, ("Edm.Binary", "Edm.Stream")),
    datetime.datetime: (parse_datetime, ("Edm.DateTimeOffset", "Edm.DateTime")),
    datetime.timedelta: (parse_duration, ("Edm.Duration",)),
    datetime.date: (parse_date, ("Edm.Date",)),
    datetime.time: (None, ("Edm.TimeOfDay", "Edm.Time")),
    dict: (None, ("Edm.Json",)),
}

#: OData primitive type name -> Python type, and the reverse (the spelled name).
PRIMITIVE_PY_TYPES: dict[str, Any] = {name: py_type for py_type, (_, names) in PRIMITIVES.items() for name in names}
PY_PRIMITIVE_NAMES: dict[type, str] = {py_type: names[0] for py_type, (_, names) in PRIMITIVES.items()}


def parser_for(py_type: Any) -> Optional[Callable[[Any], Any]]:
    """The cell parser for a Python type, from the same row that spells the type.

    ``None`` for a type that is not a primitive, or is one a cell is never read back as
    (text, binary, a JSON object) -- its own constructor is then the conversion.
    """
    row = PRIMITIVES.get(py_type)
    return row[0] if row is not None else None


def primitive_type_for(type_name: Optional[str]) -> Optional[Type]:
    """The Python type for a known OData primitive, if any."""
    if type_name is None:
        return None
    return PRIMITIVE_PY_TYPES.get(type_name)


@cache
def edm_type_name(client_type: type) -> Optional[str]:
    """The EDM name a Python class declares, or ``None`` when it declares none.

    The argument is the *class*, not an instance: a lookup must not build the thing
    it asks about, and an entity without a context cannot be built at all. It is
    annotated ``type`` rather than a union of the model base classes because
    primitives are first-class here (``ClientValueCollection(str)`` asks for
    ``"Collection(Edm.String)"``) and every generated model is produced by the code
    generator at build time — the runtime has no closed set of model classes to
    enumerate. What a declaration *is* is a protocol, documented below, not a
    hierarchy: the name is read from a class attribute, so nothing has to be
    imported to be asked.

    ``None`` is a real answer, not a failure: a type nothing named has no name to
    declare, and a marker naming a type nobody declared is worse than no marker.

    Resolution order: a primitive row in :data:`PRIMITIVE_PY_TYPES`, then the
    optional ``_odata_type_name`` class fact (a model that can be asked without an
    instance), then a plain ``entity_type_name`` string attribute (a hand-written
    declaration), and only then one cached instance.

    Args:
        client_type: a primitive Python type (``str``) or a model class.

    Returns:
        ``"Edm.String"`` for ``str``, ``"microsoft.graph.Event"`` for ``Event``.
    """
    primitive = PY_PRIMITIVE_NAMES.get(client_type)
    if primitive is not None:
        return primitive
    declared = getattr(client_type, "_odata_type_name", None)
    if declared is not None:
        return declared
    # A class may still declare the name as a plain attribute (older generated
    # values, duck-typed stubs) instead of the ``_odata_type_name`` fact.
    attribute = getattr(client_type, "entity_type_name", None)
    if isinstance(attribute, str):
        return attribute
    try:
        value = client_type()
    except TypeError:
        return None
    return getattr(value, "entity_type_name", None)


def collection_type_name(client_type: type) -> Optional[str]:
    """The ``Collection(...)`` name of an element class, or ``None`` when it declares none."""
    name = edm_type_name(client_type)
    if name is None:
        return None
    return f"Collection({name})"
