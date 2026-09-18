"""Typed field value coercion for record imports.

Maps plain source values (CSV/DataFrame cells) to the payload shapes SharePoint
expects for typed fields, driven by an explicit ``schema={column: FieldType}``.
``List.from_records(..., schema=...)`` (and the streaming conveniences) applies
this, so typed columns (choice, lookup, user, URL, geolocation, ...) can be
populated without hand-building payloads:

    lst.from_dataframe(df, schema={"Status": FieldType.Choice, "Tags": FieldType.MultiChoice})

Values already in the expected shape (a ``ClientValue``) pass through unchanged.
``None`` values and unknown/``None`` field types are left as-is, so this is safe
to apply to every cell of a record.

SharePoint has no distinct field-type kind for multi-valued lookups/users (they
are ``Lookup``/``User`` fields with ``AllowMultipleValues``), so the value's
shape decides: a list, tuple or ``"; "``-separated string becomes the multi form.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Callable, Dict, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.converters.scalars import parse_bool, parse_datetime, try_float, try_int
from office365.sharepoint.fields.geolocation_value import FieldGeolocationValue
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from office365.sharepoint.fields.multi_choice_value import FieldMultiChoiceValue
from office365.sharepoint.fields.multi_lookup_value import FieldMultiLookupValue
from office365.sharepoint.fields.multi_user_value import FieldMultiUserValue
from office365.sharepoint.fields.type import FieldType
from office365.sharepoint.fields.url_value import FieldUrlValue
from office365.sharepoint.fields.user_value import FieldUserValue

_LIST_SEPARATOR = ";"


def _as_list(value: Any) -> list[Any]:
    """Normalize a value into a list (a ``"; "`` string is split)."""
    if isinstance(value, str):
        return [part.strip() for part in value.split(_LIST_SEPARATOR) if part.strip()]
    if isinstance(value, Iterable):
        return list(value)
    return [value]


def _is_multi(value: Any) -> bool:
    """Whether a value should map to a multi-valued field."""
    return isinstance(value, (list, tuple)) or (isinstance(value, str) and _LIST_SEPARATOR in value)


def _lookup_id(value: Any) -> int:
    """Read a lookup id from a mapping (``LookupId``/``Id``) or a scalar."""
    if isinstance(value, Mapping):
        value = value.get("LookupId", value.get("Id", value.get("id")))
    return int(value)


def _lookup_value(value: Any) -> Any:
    if _is_multi(value):
        return FieldMultiLookupValue([FieldLookupValue(LookupId=_lookup_id(item)) for item in _as_list(value)])
    return FieldLookupValue(LookupId=_lookup_id(value))


def _user_value(value: Any) -> FieldUserValue:
    if isinstance(value, Mapping):
        has_id = value.get("LookupId") is not None or value.get("Id") is not None
        return FieldUserValue(
            LookupId=_lookup_id(value) if has_id else None,
            LookupValue=value.get("LookupValue"),
            Email=value.get("Email", value.get("email")),
        )
    if isinstance(value, str) and "@" in value:
        return FieldUserValue(Email=value)
    return FieldUserValue(LookupId=_lookup_id(value))


def _user(value: Any) -> Any:
    if _is_multi(value):
        return FieldMultiUserValue([_user_value(item) for item in _as_list(value)])
    return _user_value(value)


def _url(value: Any) -> FieldUrlValue:
    if isinstance(value, Mapping):
        return FieldUrlValue(Url=value.get("Url"), Description=value.get("Description"))
    if isinstance(value, (tuple, list)):
        return FieldUrlValue(Url=value[0], Description=value[1] if len(value) > 1 else None)
    return FieldUrlValue(Url=str(value))


def _geolocation(value: Any) -> FieldGeolocationValue:
    if isinstance(value, Mapping):
        return FieldGeolocationValue(Latitude=float(value["Latitude"]), Longitude=float(value["Longitude"]))
    if isinstance(value, (tuple, list)) and len(value) > 1:
        return FieldGeolocationValue(Latitude=float(value[0]), Longitude=float(value[1]))
    latitude, _, longitude = str(value).partition(",")
    return FieldGeolocationValue(Latitude=float(latitude), Longitude=float(longitude))


def _datetime(value: Any) -> Any:
    return parse_datetime(value) or value


_CONVERTERS: Dict[FieldType, Callable[[Any], Any]] = {
    FieldType.Boolean: parse_bool,
    FieldType.Integer: try_int,
    FieldType.Counter: try_int,
    FieldType.Number: try_float,
    FieldType.Currency: try_float,
    FieldType.DateTime: _datetime,
    FieldType.MultiChoice: lambda value: FieldMultiChoiceValue([str(item) for item in _as_list(value)]),
    FieldType.Lookup: _lookup_value,
    FieldType.User: _user,
    FieldType.URL: _url,
    FieldType.Geolocation: _geolocation,
}


def coerce_field_value(field_type: Optional[FieldType], value: Any) -> Any:
    """Coerce a plain value into the payload shape for ``field_type``.

    Supported: Boolean, Integer, Number/Currency, DateTime, MultiChoice, Lookup
    (single/multi), User (single/multi), URL and Geolocation. Anything else (and
    already-typed ``ClientValue`` inputs) passes through unchanged.
    """
    if field_type is None or value is None or isinstance(value, ClientValue):
        return value
    converter = _CONVERTERS.get(field_type)
    return converter(value) if converter is not None else value
