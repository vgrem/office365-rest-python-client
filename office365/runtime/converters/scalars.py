"""Type-aware scalar value conversion (the "fields" layer of the conversion stack).

Each function converts a raw value (string, JSON scalar) into its typed form —
the deserialization half of the pipeline. ``serialize_value``/``coerce_value``
in ``value.py`` build on these for object-level conversion.
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Optional, Union

_TRUE_VALUES = {"true", "1", "yes", "y"}
_FALSE_VALUES = {"false", "0", "no", "n"}

#: ISO 8601 duration, the only form ``Edm.Duration`` travels in: ``PT30M``, ``P1DT2H``.
#: Years and months are absent on purpose -- they have no ``timedelta`` equivalent.
_ISO_DURATION = re.compile(
    r"^(?P<sign>[-+])?P"
    r"(?:(?P<weeks>\d+(?:\.\d+)?)W)?"
    r"(?:(?P<days>\d+(?:\.\d+)?)D)?"
    r"(?:T"
    r"(?:(?P<hours>\d+(?:\.\d+)?)H)?"
    r"(?:(?P<minutes>\d+(?:\.\d+)?)M)?"
    r"(?:(?P<seconds>\d+(?:\.\d+)?)S)?"
    r")?$"
)


def parse_enum(enum_type: type[Enum], value: str | int) -> Any:
    """Safely converts a value to the specified enum type.

    Args:
        enum_type: The Enum class to convert to
        value: The raw value to convert

    Returns:
        The enum member, the wire value when it names a combination of members, or
        None if conversion fails
    """
    try:
        return enum_type(value)
    except ValueError:
        try:
            return enum_type[str(value)]  # fallback: lookup by name
        except KeyError:
            return _parse_flags(enum_type, value)


def _parse_flags(enum_type: type[Enum], value: Any) -> Optional[str]:
    """The wire value of a ``IsFlags`` enum, or ``None`` when it names no combination.

    A flags member set travels as the member names joined by commas
    (``"password,voice"`` -- ``authenticationMethodModes``, ``applicationDataType``),
    and no member names that combination. Resolving every part is what tells a
    combination from an unknown value: returning ``None`` here would store ``None``
    and the next payload would write it back as null, dropping a setting the service
    had reported. The string is therefore kept as the service sent it -- it is also
    what the service accepts back.
    """
    if not isinstance(value, str) or "," not in value:
        return None
    parts = [part.strip() for part in value.split(",")]
    if not all(part in enum_type.__members__ for part in parts):
        return None
    return value


def parse_bool(value: Any) -> Any:
    """Convert a value to a boolean, falling back to the raw value when unrecognized.

    Args:
        value: The raw value to convert (e.g. a CSV cell)

    Returns:
        The parsed boolean, or the original value if it can't be parsed
    """
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    return value


def parse_duration(value: Any) -> Any:
    """Convert an ISO 8601 duration to ``timedelta``, falling back to the raw value.

    ``Edm.Duration`` travels as text (``PT30M``), and a column declared
    ``timedelta`` is coerced by this. A form with no ``timedelta`` equivalent --
    ``P1M`` names a month, not thirty days -- is returned as it arrived, like an
    unrecognized boolean, so an update does not write ``None`` over a value the
    service reported.

    Args:
        value: The raw value to convert (e.g. ``"PT1H30M"``)

    Returns:
        The parsed ``timedelta``, or the original value if it can't be parsed
    """
    if isinstance(value, timedelta):
        return value
    if not isinstance(value, str):
        return value
    match = _ISO_DURATION.match(value.strip())
    if match is None:
        return value
    parts = {name: float(found) for name, found in match.groupdict().items() if found is not None and name != "sign"}
    if not parts:
        return value  # "P" and "PT" spell no duration at all
    duration = timedelta(**parts)
    return -duration if match.group("sign") == "-" else duration


def parse_int(value: Any) -> Optional[int]:
    """Convert a value to an int, returning ``None`` when absent/invalid."""
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def try_int(value: Any) -> Any:
    """Convert a value to an int, falling back to the raw value on failure."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return value


def try_float(value: Any) -> Any:
    """Convert a value to a float, falling back to the raw value on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def normalize_guid(value: Any) -> Optional[str]:
    """A GUID in its canonical lower-case form, or ``None`` when the value is not one.

    One identifier is spelled several ways across SharePoint: bare in a JSON payload,
    ``{...}`` in a column's ``SchemaXml``, in either case — so two ids that name the
    same list compare unequal unless both sides are normalized first. ``uuid.UUID`` is
    the parser: it accepts the brace, ``urn:uuid:`` and 32-hex forms too, and answers
    the ``8-4-4-4-12`` spelling.
    """
    if value is None:
        return None
    try:
        return str(uuid.UUID(str(value).strip()))
    except ValueError:
        return None


def utc_now_iso() -> str:
    """Current UTC time as an ISO-8601 string (second precision)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_aware_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Return ``value`` as a timezone-aware UTC datetime.

    Values created locally (for example when adding a credential) may carry no
    ``tzinfo``. Comparing such naive datetimes against :func:`datetime.now`
    (UTC) raises ``TypeError``; treat them as UTC instead.
    """
    if value is not None and value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def iso(value: Any) -> str:
    """ISO-8601 string for a datetime (second precision); ``""`` for ``None``."""
    if value is None:
        return ""
    return value.isoformat(timespec="seconds")


def iso_or_none(value: Any) -> Optional[str]:
    """ISO-8601 string for a datetime, or ``None`` when unset/absent.

    Treats ``datetime.min`` (the "not loaded" sentinel used by some SharePoint
    properties) as unset.
    """
    if value is None or value == datetime.min:
        return None
    return value.isoformat(timespec="seconds") if hasattr(value, "isoformat") else (str(value) or None)


def iso_z(value: Any) -> Optional[str]:
    """UTC ISO-8601 string with a ``Z`` suffix (second precision); ``None`` when unset.

    SharePoint and Microsoft Graph parse date-time strings on the wire as UTC
    with a trailing ``Z``; some endpoints (for example ``ShareLink``) reject a
    numeric offset such as ``+00:00`` as an invalid date. Naive datetimes are
    assumed to be UTC.

    A string is parsed first -- ``ValidateUpdateListItem(dates_in_utc=True)``, the
    only REST path that writes ``Created``/``Modified``, takes one -- and a string
    that cannot be read is passed through unchanged, so the service rejection names
    the value instead of this layer having dropped it.
    """
    if isinstance(value, str):
        parsed = parse_datetime(value)
        if parsed is None:
            return value or None
        value = parsed
    if value is None:
        return None
    if value.tzinfo is not None:
        value = value.astimezone(timezone.utc)
    return value.replace(tzinfo=None).isoformat(timespec="seconds") + "Z"


def _normalize_datetime_string(value: str) -> str:
    """Truncate or pad fractional seconds to exactly 6 digits for %f compatibility."""
    if "." not in value:
        return value
    before, _, after = value.partition(".")
    tz_marker = ""
    for marker in ("Z", "+", "-"):
        if marker in after:
            index = after.find(marker)
            tz_marker = after[index:]
            after = after[:index]
            break
    frac = after[:6].ljust(6, "0")
    return f"{before}.{frac}{tz_marker}"


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
        "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 with numeric offset
        "%Y-%m-%dT%H:%M:%S.%f%z",  # ISO 8601 with microseconds and offset
        "%Y-%m-%d",  # Date only
    ]

    if isinstance(value, str):
        value = _normalize_datetime_string(value)

    for fmt in known_formats:
        try:
            result = datetime.strptime(value, fmt)
            if result.tzinfo is None and fmt.endswith("Z"):
                result = result.replace(tzinfo=timezone.utc)
            return result
        except ValueError:
            continue
    # Anything ISO-8601 the fixed list does not spell (a space separator, no
    # seconds, ...). The fraction is normalized first, so this answers the same
    # thing on every supported interpreter: ``fromisoformat`` only learned to
    # accept more than six fractional digits in 3.11, and a .NET stamp carries
    # seven.
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def wall_clock(value: Any) -> Optional[datetime]:
    """A Graph date-time as a naive *wall clock*, or ``None``.

    A Graph ``dateTime`` is paired with its zone in a separate ``timeZone`` property, so the
    literal is the wall clock: any offset it carries is dropped, not converted (``09:00+02:00``
    and ``09:00`` with ``timeZone: "Europe/Helsinki"`` are the same appointment). A date-only
    literal -- a recurrence ``endDate``, a birthday -- names no moment and answers ``None``.

    The parsing itself is :func:`parse_datetime`, which settles the fraction width and the
    formats; the two callers that need a wall clock (``Compare(format="wall-clock")`` for a
    digest, the ``.ics`` writer for ``DTSTART``/``DTEND``/``UNTIL``) format this value their
    own way.
    """
    text = str(value or "").strip()
    if "T" not in text:
        return None
    parsed = parse_datetime(text)
    return parsed.replace(tzinfo=None) if parsed else None


def wall_clock_text(value: Any) -> Optional[str]:
    """A naive ``YYYY-MM-DD HH:MM:SS`` literal for a date, or for text a service returned.

    This is the form a SharePoint *document* item accepts: it ignores ``datesInUTC``
    and parses every date string in the web's locale, rejecting a trailing ``Z``
    ("...must specify a valid date within the range of 1/1/1900 and 12/31/8900.").
    The literal names a wall clock, so a caller converts the instant to web-local
    time first (``TimeZone.utc_to_local_time``) rather than this function guessing a
    zone.

    Text is passed through as the service spelled it: a value that is already local,
    or an unreadable literal, must not be reshaped here.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)
