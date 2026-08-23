"""Value-level conversion between stored values and their JSON representation.

The serialization half of the conversion layer: ``serialize_value`` maps any
stored value to its JSON form (shared by ``ClientObject``/``ClientValue``/
``ClientValueCollection`` ``to_json``), and ``_add_type_metadata`` attaches the
OData type marker. The deserialization half (``coerce_value``/``declared_type``)
will live here too.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, Optional

from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.odata.v3.json_light_format import JsonLightFormat


def serialize_value(value: Any, json_format: Optional[ODataJsonFormat] = None) -> Any:
    """Convert a stored value to its JSON representation.

    Enums become their value, datetimes/dates ISO 8601, bytes decoded to UTF-8,
    UUIDs strings, and nested objects serialized via their ``to_json``. Any other
    value (scalar, ``None``, ``dict``, ``list``) passes through unchanged.
    """
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, bytes):
        return value.decode("utf-8")
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if hasattr(value, "to_json"):
        return value.to_json(json_format)
    return value


def _add_type_metadata(
    result: Dict[str, Any], json_format: Optional[ODataJsonFormat], entity_type_name: Optional[str]
) -> None:
    """Attach the OData type metadata marker when the format requests it."""
    if json_format is not None and json_format.include_control_information and entity_type_name is not None:
        if isinstance(json_format, JsonLightFormat):
            result[json_format.metadata_type] = {"type": entity_type_name}
        elif isinstance(json_format, ODataJsonFormat):
            result[json_format.metadata_type] = "#" + entity_type_name
