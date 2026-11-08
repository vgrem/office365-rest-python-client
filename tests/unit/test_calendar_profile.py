"""The calendar's spelling is data: pinned tables, a golden document, a stable digest.

Three things are asserted here, all of them about *where* an answer lives rather than
what one particular export happened to write:

* every :class:`IcsDialect` row names a member its generated enum declares — a token for a
  word the service never sends is a lie, and a renamed member is a row that silently
  stops matching;
* the tables that are meant to be complete cover their enum, so a value the service gains
  cannot quietly render as nothing;
* what a digest sees is the model's own comparable form (``to_json(COMPARABLE)``), and an
  option keeps a field out of the verification when the import declines to restore it.

The golden document is the codec's whole contract in one assertion: line order, folding
at 75 octets, and which token each Graph word became. It is a file beside its sidecar
(``fixtures/outlook/``) rather than a literal here, so a change to the writer shows up as a
line diff in review and not as a rewritten wall of escapes.
"""

from __future__ import annotations

import hashlib
import json

import pytest
from office365.migration.outlook.calendar_codec import encode, rrule
from office365.migration.outlook.calendar_models import CalendarImportOptions, EventRecord
from office365.migration.outlook.calendar_profile import ICALENDAR
from office365.outlook.calendar.attendees.type import AttendeeType
from office365.outlook.calendar.dayofweek import DayOfWeek
from office365.outlook.calendar.events.sensitivity import Sensitivity
from office365.outlook.calendar.meetingtimes.freebusystatus import FreeBusyStatus
from office365.outlook.mail.body_type import BodyType
from office365.outlook.mail.importance import Importance
from office365.outlook.mail.messages.responsetype import ResponseType
from office365.outlook.mail.recurrencepatterntype import RecurrencePatternType
from office365.outlook.mail.weekindex import WeekIndex
from tests.unit.outlook_fixtures import document, sidecar

#: The dialect as a table: (the mapping, the generated enum it must agree with, whether
#: every member carries a token). ``transp``/``status`` are the two that spell only what a
#: reader cannot assume — a busy event carries no ``TRANSP``, an accepted one no ``STATUS``.
TABLES = [
    (ICALENDAR.transp, FreeBusyStatus, False),
    (ICALENDAR.status, FreeBusyStatus, False),
    (ICALENDAR.classification, Sensitivity, True),
    (ICALENDAR.priority, Importance, True),
    (ICALENDAR.role, AttendeeType, True),
    (ICALENDAR.partstat, ResponseType, True),
    (ICALENDAR.weekdays, DayOfWeek, True),
    (ICALENDAR.week_index, WeekIndex, True),
    (ICALENDAR.frequency, RecurrencePatternType, True),
    (ICALENDAR.body_field, BodyType, True),
]

#: A sidecar with one of everything, so the golden document exercises every branch the
#: writer has: an escaped subject, an HTML body, an attendee with and without a name,
#: categories, a classification, a reminder, and a join URL long enough to fold. The keys
#: are the model's own (``Event.to_json()``) plus the export's provenance.
SIDECAR = sidecar("quarterly_review")


def _digest(envelope, options=None) -> str:
    """The digest of a sidecar envelope, read back the way an import reads it."""
    return EventRecord.from_json(envelope).digest(options)


def test_the_codec_renders_the_golden_document():
    """The whole contract in one assertion: order, folding, and every token's spelling."""
    assert encode(SIDECAR) == document("quarterly_review.ics")


@pytest.mark.parametrize(
    ("pattern", "expected"),
    [
        ({"type": "daily", "interval": 3}, "FREQ=DAILY;INTERVAL=3"),
        ({"type": "weekly", "daysOfWeek": ["monday", "wednesday"]}, "FREQ=WEEKLY;BYDAY=MO,WE"),
        ({"type": "absoluteMonthly", "dayOfMonth": 15}, "FREQ=MONTHLY;BYMONTHDAY=15"),
        (
            {"type": "relativeMonthly", "daysOfWeek": ["tuesday"], "index": "last"},
            "FREQ=MONTHLY;BYDAY=-1TU",
        ),
        ({"type": "absoluteYearly", "month": 3, "dayOfMonth": 2}, "FREQ=YEARLY;BYMONTH=3;BYMONTHDAY=2"),
        (
            {"type": "relativeYearly", "month": 11, "daysOfWeek": ["thursday"], "index": "first"},
            "FREQ=YEARLY;BYMONTH=11;BYDAY=1TH",
        ),
    ],
)
def test_the_frequency_table_spells_every_pattern_the_service_sends(pattern, expected):
    assert rrule({"pattern": pattern, "range": {"type": "noEnd"}}) == expected


@pytest.mark.parametrize(("mapping", "enum", "complete"), TABLES)
def test_every_dialect_row_names_a_member_the_enum_declares(mapping, enum, complete):
    """A key the enum does not declare is a token for a word the service never sends.

    The generated Graph enums are numeric on the wire, so the member's *name* is the
    Graph word — that is what a dialect row is keyed by.
    """
    declared = {member.name for member in enum}
    assert set(mapping) <= declared
    assert not complete or declared <= set(mapping)


def test_the_digest_is_stable_across_the_split():
    """A sidecar's digest is computed by both sides of an import, so it must not drift."""
    assert _digest(SIDECAR) == "79a81fa4bdc5daa7465a055d8f0c8a59"


def test_the_comparable_form_is_what_the_sender_stated():
    form = EventRecord.from_json(SIDECAR).canonical(CalendarImportOptions(restore_attendees=True))
    assert form["start"] == {"dateTime": "2026-03-02T09:00:00", "timeZone": "Europe/Kiev"}
    assert form["body"] == {"content": "Agenda: Q1"}
    assert form["attendees"] == [
        {"emailAddress": {"address": "bob@contoso.com", "name": "Bob"}, "type": "required"},
        {"emailAddress": {"address": "carol@contoso.com", "name": "carol@contoso.com"}, "type": "optional"},
    ]
    assert not {"id", "iCalUId", "organizer", "webLink", "ics_path"} & form.keys()


def test_a_gated_field_leaves_the_digest_when_the_import_declines_to_restore_it():
    options = CalendarImportOptions(restore_attendees=False)
    someone_else = [{"emailAddress": {"address": "someone@else.test"}, "type": "required"}]
    assert _digest(SIDECAR, options) == _digest({**SIDECAR, "attendees": someone_else}, options)
    restoring = CalendarImportOptions(restore_attendees=True)
    assert _digest(SIDECAR, restoring) != _digest({**SIDECAR, "attendees": someone_else}, restoring)


def test_the_digest_is_the_md5_of_the_canonical_form():
    canonical = json.dumps(EventRecord.from_json(SIDECAR).canonical(), sort_keys=True, default=str)
    assert _digest(SIDECAR) == hashlib.md5(canonical.encode("utf-8")).hexdigest()
