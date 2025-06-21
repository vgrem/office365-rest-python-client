import mimetypes
import warnings
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Any, Dict, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse


def is_absolute_url(url: str) -> bool:
    """Determine if a URL is absolute (contains network location)."""
    return bool(urlparse(url).netloc)


def get_absolute_url(url: str) -> str:
    """Extract the base URL (scheme+netloc) from a full URL.

    Example:
        >>> get_absolute_url("https://example.com/path?query=1")
        'https://example.com'
    """
    path = urlparse(url).path
    return url.replace(path, "")


def parse_query_param(url: str, key: str) -> str:
    """Extract the first value of a query string parameter.

    Args:
        url: URL containing query string
        key: Query parameter key to look up

    Returns:
        First value for the specified key

    Raises:
        KeyError: If parameter not found
    """
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)[key][0]


def get_mime_type(file_name: str) -> tuple[str, str]:
    """Guess the MIME type and encoding for a filename.

    Returns:
        Tuple of (type, encoding) where either may be None
    """
    return mimetypes.guess_type(file_name)


def deprecated(reason: str, version: str = "next"):
    """Mark functions/methods as deprecated with a warning.

    Args:
        reason: Explanation why this is deprecated
        version: Version when this will be removed
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated and will be removed in v{version}. {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def parse_enum(enum_type: type[Enum], value: int) -> Optional[Enum]:
    """Safely converts a value to the specified enum type.

    Args:
        enum_type: The Enum class to convert to
        value: The raw value to convert

    Returns:
        The enum member or None if conversion fails
    """
    try:
        return enum_type(value)
    except ValueError:
        import warnings

        warnings.warn(
            f"Invalid value '{value}' for enum {enum_type.__name__}",
            RuntimeWarning,
            stacklevel=2,
        )
        return None


def parse_datetime(value: Union[str, datetime, None]) -> Optional[datetime]:
    """
    Converts string representations of Edm.DateTime/Edm.DateTimeOffset to datetime.

    Args:
        value: Input value (string, datetime, or None)

    Returns:
        Parsed datetime or None if conversion fails

    Examples:
        >>> parse_datetime("2023-01-01T12:00:00Z")
        datetime.datetime(2023, 1, 1, 12, 0)
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value

    known_formats = [
        "%Y-%m-%dT%H:%M:%SZ",  # ISO 8601 UTC
        "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 with microseconds
        "%Y-%m-%dT%H:%M:%S",  # Without timezone
        "%Y-%m-%dT%H:%M:%S.%f",  # With microseconds no TZ
        "%Y-%m-%d",  # Date only
    ]

    for fmt in known_formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


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
        return key, conversions[value_type](raw_value)
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
        >>> parse_key_value_collection({
        ...     0: {'Key': 'UserProfile_GUID', 'Value': 'd895ff01...', 'ValueType': 'Edm.String'},
        ...     1: {'Key': 'IsAdmin', 'Value': 'true', 'ValueType': 'Edm.Boolean'}
        ... })
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
