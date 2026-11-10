"""Value-level conversion between stored values and their JSON representation.

The shared conversion layer: ``serialize_value`` maps stored values to their JSON
form (used by ``ClientObject``/``ClientValue``/``ClientValueCollection``
``to_json``), and ``deserialize_value`` maps raw values to their declared type
(used by ``set_property``). Which type that is, is a schema fact: ``declared_type``
asks the type's ``dtypes``. Control information is not this layer's business: a
profile attaches it (``JsonProfile.wrap``).
"""

from __future__ import annotations

import uuid
from datetime import date, datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, get_origin

from office365.runtime.converters.scalars import deserialize_enum, parse_datetime
from office365.runtime.odata.edm import parser_for
from office365.runtime.schema import TypeSchema
from office365.runtime.types.duration import Duration

if TYPE_CHECKING:
    from office365.runtime.odata.json_format import JsonProfile

_UNSET = object()


def _serialize_enum(value: Enum, profile: Optional[JsonProfile]) -> Any:
    """Serialize an enum member for the active OData dialect.

    OData V3 (SharePoint) enums travel as their numeric value
    (``FieldTypeKind`` is ``Edm.Int32``); OData V4 / Graph enums travel as
    the member *name* ("teamsForBusiness") — the dialect says which. Enums
    generated with string values already match their name; older Graph ones
    (e.g. auto-numbered ``unknown = 0``) must fall back to the name, not the
    ordinal.

    A generated Graph enum carries the *CSDL ordinal* as a string
    (``TaskStatus.completed = "2"``), which is not a wire value — Graph
    rejects it, so a digit-only string falls back to the member name too.
    """
    if profile is not None and not profile.dialect.enum_by_name and isinstance(value.value, int):
        return value.value
    if isinstance(value.value, str):
        return value.name if value.value.isdigit() else value.value
    return value.name


def serialize_value(  # noqa: PLR0911 - one return per stored-value kind
    value: Any, profile: Optional[JsonProfile] = None, *, skip_none: bool = False
) -> Any:
    """Convert a stored value to its JSON representation.

    Handles ``ClientObject``/``ClientValue``/``ClientValueCollection`` (via their
    ``to_json``), ``Enum`` -> value, ``datetime``/``date`` -> ISO 8601, ``bytes``
    -> UTF-8, ``UUID`` -> str. A plain ``dict``/``list``/``tuple`` is descended into,
    so a container assembled by hand (a nested payload, a ``to_json`` result, a
    request body) is as JSON-safe as a generated value. Any other value (scalar,
    ``None``, ``ClientResult``) passes through unchanged.

    ``to_json`` is consulted *before* the container branches: a collection type may
    subclass ``dict``/``list`` and still need its own serialization.

    ``skip_none`` drops a ``None`` member of a container: a request body states
    "not provided" by omission, a document does not.
    """
    if value is None:
        return value
    value_type = type(value)
    if value_type is str or value_type is int or value_type is bool or value_type is float:
        return value
    if isinstance(value, Enum):
        return _serialize_enum(value, profile)
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, timedelta):
        return Duration.parse(value)
    if hasattr(value, "to_json"):
        return value.to_json(profile)
    if isinstance(value, dict):
        return {
            k: serialize_value(item, profile, skip_none=skip_none)
            for k, item in value.items()
            if not (skip_none and item is None)
        }
    if isinstance(value, (list, tuple)):
        return [serialize_value(item, profile, skip_none=skip_none) for item in value]
    return value


def declared_type(cls: type, name: str) -> Any:
    """The type a column of ``cls`` is declared as, as its schema states it.

    ``None`` when the type declares no such column. Every source of a declaration --
    a getter's return annotation, a dataclass field -- is read once, by the schema.
    """
    return TypeSchema.of(cls).dtypes[name]


def deserialize_declared(value: Any, declared: Any) -> Any:
    """Deserialize a raw value as a declared scalar or enum type.

    Returns ``_UNSET`` when the declared type isn't a supported scalar/enum, so
    callers can fall back to their own handling.
    """
    converter = parser_for(declared)
    if converter is not None:
        return converter(value)
    if isinstance(declared, type) and issubclass(declared, Enum):
        return deserialize_enum(declared, value)
    return _UNSET


def deserialize_nested(base: Any, value: Any, persist_changes: bool) -> Any:
    """Apply a raw list/dict onto a nested ``ClientValue``/``ClientObject``
    (whose ``set_property`` maps list items by index and dict items by key),
    returning the stored value. Scalar values are returned as-is.
    """
    if isinstance(value, list):
        for i, p_v in enumerate(value):
            base.set_property(i, p_v, persist_changes)
    elif isinstance(value, dict):
        for k, p_v in value.items():
            base.set_property(k, p_v, persist_changes)
    else:
        return value
    return base


def values_of(value: Any) -> Optional[list[Any]]:
    """A collection cell as a plain list, in every shape a read or a payload produces.

    A ``$select`` read of an undeclared collection column ingests the JSON
    ``{"results": [...]}`` as a positional mapping (``{0: 1, 1: 2}``), a declared one
    as a ``ClientValueCollection``, a payload this client built may hold either the
    wrapper or a bare list, and a single-valued cell may hold one scalar. A dict that
    is neither a container nor positional is one value object, not a list of its
    fields.

    Returns ``None`` for ``None`` so a caller can tell "no value" from "no values".
    """
    if value is None:
        return None
    items: list[Any]
    if isinstance(value, dict):
        if isinstance(value.get("results"), (list, tuple)):
            items = list(value["results"])
        elif value and all(isinstance(key, int) for key in value):
            items = [value[key] for key in sorted(value)]
        else:
            items = [value]
    elif isinstance(value, (str, bytes)):
        items = [value]
    elif isinstance(value, (list, tuple, set)):
        items = list(value)
    elif hasattr(value, "_data") and isinstance(value._data, list):
        items = list(value._data)
    else:
        items = [value]
    return items


def deserialize_value(target_type: Any, value: Any, current: Any, persist_changes: bool) -> Any:
    """Deserialize a raw value for storage by its declared type, falling back to the current one.

    Declared scalars/enums go through ``deserialize_declared``; declared
    ``ClientValue``/``ClientValueCollection`` (including generic aliases) are
    populated via ``deserialize_nested``. Otherwise the value is deserialized against
    the current instance (a nested ``ClientObject``/``ClientValue``, ``datetime``,
    ``Enum``) or passed through raw.
    """
    if target_type is not None and value is not None:
        from office365.runtime.client_value import ClientValue  # local: it imports this module

        deserialized = deserialize_declared(value, target_type)
        if deserialized is not _UNSET:
            return deserialized
        origin = target_type if isinstance(target_type, type) else get_origin(target_type)
        if isinstance(origin, type) and issubclass(origin, ClientValue):
            if not isinstance(current, origin):
                current = origin()
            return deserialize_nested(current, value, persist_changes)
    if hasattr(current, "set_property") and not isinstance(current, (datetime, Enum)):
        return deserialize_nested(current, value, persist_changes)
    if isinstance(current, datetime):
        return parse_datetime(value)
    if isinstance(current, Enum):
        return current if value is None else deserialize_enum(type(current), value)
    return value
