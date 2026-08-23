"""SharePoint Edm key-value pair conversion.

Converts ``{Key, Value, ValueType}`` structures (from SharePoint search and
user profiles) into typed Python values.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, Optional, Tuple, Union

from office365.runtime.converters.scalars import parse_datetime


def parse_key_value(value: Dict[str, Any]) -> Tuple[Optional[str], Any]:
    """Parses SharePoint key-value pairs with type conversion and warnings.

    Args:
        value: Dictionary containing:
            - Key: The field name
            - Value: The raw value to convert
            - ValueType: The OData type descriptor

    Returns:
        Tuple of (original_key, converted_value). Returns original values on failure.

    Warnings:
        RuntimeWarning: When type conversion fails
    """
    key = value.get("Key")
    raw_value = value.get("Value")
    value_type = value.get("ValueType")

    # Early return for missing data
    if None in (key, value_type, raw_value):
        return key, raw_value

    # Type conversion mapping
    conversions = {
        "Edm.Int64": int,
        "Edm.Int32": int,
        "Edm.Double": float,
        "Edm.Boolean": lambda v: v.lower() == "true",
        "Edm.Binary": bytes.fromhex,
        "Edm.DateTime": parse_datetime,
        "Edm.Guid": str,
    }

    if value_type not in conversions:
        return key, raw_value

    try:
        return key, conversions[value_type](raw_value)  # type: ignore
    except (ValueError, AttributeError, TypeError) as e:
        warnings.warn(
            f"Failed to convert {key!r} (type {value_type}): {str(e)}",
            RuntimeWarning,
            stacklevel=2,  # Points to caller's line
        )
        return key, raw_value


def parse_key_value_collection(
    value: Dict[int, Dict[str, Any]],
) -> Dict[str, Union[str, int, float, bool, bytes]]:
    """Converts a SharePoint KeyValue collection to a Python dictionary with proper type conversion.

    Args:
        value: Dictionary in format {index: {'Key':..., 'Value':..., 'ValueType':...}}

    Returns:
        Dictionary with {key: converted_value} pairs

    Examples:
        >>> parse_key_value_collection(
        ...     {
        ...         0: {"Key": "UserProfile_GUID", "Value": "d895ff01...", "ValueType": "Edm.String"},
        ...         1: {"Key": "IsAdmin", "Value": "true", "ValueType": "Edm.Boolean"},
        ...     }
        ... )
        {'UserProfile_GUID': 'd895ff01...', 'IsAdmin': True}
    """
    result = {}
    for item in value.values():
        try:
            key, converted_value = parse_key_value(item)
            if key is not None:  # Only add if key exists
                result[key] = converted_value
        except (KeyError, ValueError, TypeError) as e:
            warnings.warn(
                f"Skipping malformed KeyValue entry: {str(e)}",
                RuntimeWarning,
                stacklevel=2,
            )
    return result
