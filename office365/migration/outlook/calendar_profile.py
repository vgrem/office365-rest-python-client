"""The calendar's vocabulary as data: Graph's words, and the tokens they become.

Nothing here decides *when* a token is written — that is the codec's job — and nothing
here knows about a client: these are tables, so the answer to "what does a
tentatively-accepted attendee look like in an ``.ics``" is a row, not a branch.

:class:`IcsDialect` is the ``.ics`` spelling: one table per generated Graph enum the
writer speaks. Each is checked against its enum by ``tests/unit/test_calendar_profile.py``
— a row naming a member the model does not declare fails the suite, because a token for
a word the service never sends is a lie. ``transp`` and ``status`` are deliberately
*partial*: a busy event carries no ``TRANSP`` and an accepted one no ``STATUS``, since
those are what a reader assumes by default, so their incompleteness is the spelling
rather than an omission.

What a digest compares is not spelled here: the model declares what the service treats as
the same value (``Compare`` on the field) and ``to_json(CANONICAL)`` applies it.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class IcsDialect:
    """How one calendar dialect spells Graph's words — RFC 5545 names, by table."""

    #: Graph ``showAs`` → ``TRANSP``: only a free event is transparent.
    transp: Mapping[str, str]
    #: Graph ``showAs`` → ``STATUS``: only a tentative event carries one.
    status: Mapping[str, str]
    #: Graph ``sensitivity`` → ``CLASS``.
    classification: Mapping[str, str]
    #: Graph ``importance`` → ``PRIORITY`` (1 highest, 5 normal, 9 lowest).
    priority: Mapping[str, str]
    #: Graph attendee ``type`` → ``ROLE``.
    role: Mapping[str, str]
    #: Graph attendee ``status.response`` → ``PARTSTAT``.
    partstat: Mapping[str, str]
    #: Graph ``dayOfWeek`` → RFC 5545 weekday abbreviation.
    weekdays: Mapping[str, str]
    #: Graph ``pattern.index`` → the ordinal prefix of a ``BYDAY`` value.
    week_index: Mapping[str, str]
    #: Graph ``pattern.type`` → the ``FREQ`` that pattern expresses.
    frequency: Mapping[str, str]
    #: Graph body ``contentType`` → the property the text is written to.
    body_field: Mapping[str, str]


#: The dialect this writer speaks. A second dialect — ``METHOD:REQUEST`` for an
#: invitation, a different ``PARTSTAT`` default — is another row, not another writer.
ICALENDAR = IcsDialect(
    transp=MappingProxyType({"free": "TRANSPARENT"}),
    status=MappingProxyType({"tentative": "TENTATIVE"}),
    classification=MappingProxyType(
        {"normal": "PUBLIC", "personal": "PRIVATE", "private": "PRIVATE", "confidential": "CONFIDENTIAL"}
    ),
    priority=MappingProxyType({"high": "1", "normal": "5", "low": "9"}),
    role=MappingProxyType({"required": "REQ-PARTICIPANT", "optional": "OPT-PARTICIPANT", "resource": "NON-PARTICIPANT"}),
    partstat=MappingProxyType(
        {
            "none": "NEEDS-ACTION",
            "organizer": "ACCEPTED",
            "tentativelyAccepted": "TENTATIVE",
            "accepted": "ACCEPTED",
            "declined": "DECLINED",
            "notResponded": "NEEDS-ACTION",
        }
    ),
    weekdays=MappingProxyType(
        {
            "sunday": "SU",
            "monday": "MO",
            "tuesday": "TU",
            "wednesday": "WE",
            "thursday": "TH",
            "friday": "FR",
            "saturday": "SA",
        }
    ),
    week_index=MappingProxyType({"first": "1", "second": "2", "third": "3", "fourth": "4", "last": "-1"}),
    frequency=MappingProxyType(
        {
            "daily": "DAILY",
            "weekly": "WEEKLY",
            "absoluteMonthly": "MONTHLY",
            "relativeMonthly": "MONTHLY",
            "absoluteYearly": "YEARLY",
            "relativeYearly": "YEARLY",
        }
    ),
    # iCalendar's ``DESCRIPTION`` is TEXT; HTML rides in the standard ``X-ALT-DESC``,
    # which a client that does not understand it still shows as a plain description.
    body_field=MappingProxyType({"html": "X-ALT-DESC;FMTTYPE=text/html", "text": "DESCRIPTION"}),
)


def display_name(value: Mapping[str, Any] | None) -> str:
    """A Graph ``{"displayName": …}`` object as the text it carries (a location)."""
    return str((value or {}).get("displayName") or "")


__all__ = [
    "ICALENDAR",
    "IcsDialect",
    "display_name",
]
