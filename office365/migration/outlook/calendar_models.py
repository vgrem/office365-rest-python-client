"""Calendar records — one event's sidecar, and the artefacts a migration builds from it.

An exported event is two files: an ``.ics`` (the portable artefact — Outlook, Google
Calendar and Thunderbird all open it) and a JSON sidecar carrying what iCalendar cannot
express faithfully (Graph ids, the recurrence object Graph normalises, the online-meeting
provider, sensitivity/importance). The sidecar is the import contract; the ``.ics`` is
regenerated from it, so an export is reproducible: the same event always produces the
same bytes.

The sidecar **is the event as the model serializes it** — ``event.to_json()`` plus the
three things no model can know (the calendar it came from, the path it is written to,
and that calendar's display path). So nothing here lists a field: a column the model
declares is exported, replayed and verified with no function edited, and the keys are
Graph's own spellings (``isAllDay``, ``showAs``, ``iCalUId``) because that is what the
model answers and what an import posts back. The convention itself is
:class:`office365.migration.outlook.records.SidecarRecord`, shared with the mailbox and
contacts families.

Spelling lives in two tables, not here: which iCalendar token a Graph value becomes is
:mod:`office365.migration.outlook.calendar_profile`, and the document itself is written
by :mod:`office365.migration.outlook.calendar_codec`.

Unlike mail, this file is *built* rather than fetched, so a byte checksum is a valid
verification of an export: there is no server re-serialization in the middle. An
*import* is the other way round — Exchange re-serializes what it accepts and assigns the
meeting metadata — so it is verified by a digest of the event's restorable fields
(:meth:`EventRecord.digest`).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple, cast

from office365.migration.outlook.calendar_codec import MAX_LINE_OCTETS, encode
from office365.migration.outlook.records import SidecarRecord
from office365.migration.outlook.restore import restores, withheld
from office365.outlook.calendar.events.event import Event
from office365.runtime.odata.comparable import COMPARABLE
from office365.runtime.odata.v4.json_format import V4JsonFormat

#: Graph event properties an export reads: every column the model declares.
#: Derived rather than listed, so a $select cannot disagree with the getters that
#: consume it — the class of bug that produced ``iCalUid`` (one capital short of
#: the real ``iCalUId``, silently ``None``) is now unrepresentable. Navigation
#: properties are excluded by construction: ``$select`` rejects them.
EVENT_COLUMNS = Event.select_all()

#: Keys a sidecar written before the envelope became the model's own JSON carries. Their
#: presence means the tree was exported by a version that spelled its own vocabulary
#: (``graph_id``/``is_all_day``), and reading it as Graph's would silently find nothing.
LEGACY_KEYS = ("graph_id", "is_all_day", "show_as", "ical_uid")


@dataclass
class CalendarExportOptions:
    """What a calendar export includes."""

    #: Name of the top folder in the export tree (``None`` uses the calendar's own
    #: display name, slugified). Set it to keep a stable root across renames.
    root_name: str | None = None
    #: Export the individual occurrences/exceptions of a recurring event as well as
    #: the series. Off by default: a series already carries its pattern, and each
    #: instance copied as a standalone event would show up twice in the target.
    include_recurring_instances: bool = False
    #: Export cancelled events. Off by default: a cancelled event is a tombstone,
    #: and the import creates live events, so replaying one would resurrect a
    #: meeting the user cancelled.
    include_cancelled: bool = False
    #: Extra Graph event properties to record in the sidecar (camelCase names).
    extra_properties: list[str] = field(default_factory=list)


@dataclass
class CalendarImportOptions:
    """What an import of an exported calendar restores.

    Pass the *same* options object to both adapters of an import job: the source
    computes the content digest of what the target promises to restore, so the two
    sides have to agree on the fields to be comparable (see :meth:`EventRecord.digest`).
    """

    #: Re-add the attendee list. **Off by default**, because creating an event with
    #: attendees makes Exchange send an invitation to every one of them (measured:
    #: a copy lands in the organizer's Sent Items, and ``responseRequested: false``
    #: does not suppress it) — so a historical import would spam colleagues with
    #: meetings they already had. With it off the attendees stay in the sidecar and
    #: the run reports how many were dropped.
    restore_attendees: bool = restores("attendees", default=False)
    #: Re-apply the category labels.
    restore_categories: bool = restores("categories", default=True)
    #: Give every created event a deterministic ``transactionId``, so two concurrent
    #: runs of the same import collide on the server rather than both writing.
    use_transaction_ids: bool = True


#: What verifies an import: the event as its sender stated it. The other writable columns
#: (``transactionId``, ``isOnlineMeeting``, ``hideAttendees``) legitimately differ after a create.
_VERIFIED = (
    "subject",
    "start",
    "end",
    "is_all_day",
    "location",
    "locations",
    "show_as",
    "sensitivity",
    "importance",
    "is_reminder_on",
    "reminder_minutes_before_start",
    "recurrence",
    "body",
    "attendees",
    "categories",
)
assert all(Event.odata_name(attr) for attr in _VERIFIED)  # a misspelt name fails here, not at the first digest


class EventRecord(SidecarRecord):
    """One event as the export records it: Graph's payload, where it came from, its artefacts.

    ``ics`` is the portable document, ``payload`` the create body an import posts, and
    ``digest``/``checksum`` what a verification compares on either side.
    """

    model = Event
    item_type = "event"
    content_suffix = ".ics"
    provenance = ("calendar_path", "calendar_display_path", "ics_path")
    legacy_keys = LEGACY_KEYS
    legacy_name = "calendar"
    identity = ("id", "ical_uid")
    label = "subject"
    file_stamp_from = ("start",)
    modified_from = ("last_modified_date_time",)
    created_from = ("created_date_time", "last_modified_date_time")
    verified = _VERIFIED
    columns = EVENT_COLUMNS
    options_class = CalendarImportOptions

    @property
    def event(self) -> Event:
        """The model this record was built from, or read back into."""
        return cast("Event", self._entity)

    def ics(self) -> bytes:
        """The event as an ``.ics`` document (see the codec's :func:`encode`)."""
        return encode(self.envelope)

    def payload(self, options: CalendarImportOptions | None = None) -> Dict[str, Any]:
        """The Graph ``POST /events`` body for this record.

        The model spells the body: ``to_json`` with a request profile emits what a create
        may send, dropping what the service owns (``@odata(readonly=True)``: the id, the
        organizer, the attendee responses, the audit stamps) and the ``extra_properties``
        an export records only to survive a round trip. What is left is exactly what an
        import may restore; the options then decide how much of it to send. Nothing here
        spells a Graph field.
        """
        options = self.options_class() if options is None else options
        spelled = self.event.to_json(V4JsonFormat("none").scoped(Event, without=withheld(options)))
        body: Dict[str, Any] = {
            name: value
            for name, value in spelled.items()
            # The model's own vocabulary, and only what it can actually say: an undeclared
            # key is provenance an export records for its ledger, and a null/empty value is
            # the absence of a statement, not a request to clear a field.
            if name in Event._schema.properties and value not in (None, {}, [])
        }
        start, end = body.get("start") or {}, body.get("end") or {}
        if not start.get("dateTime") or not end.get("dateTime"):
            raise ValueError("the sidecar has no start/end dateTime: an event cannot be created without a time range")
        if isinstance(body.get("recurrence"), str):
            raise ValueError(
                f"the sidecar records the recurrence as text ({body['recurrence'][:60]!r}): it was written by a"
                " version of the exporter that serialised Graph's typed object with ``repr``, so the series cannot"
                " be replayed — re-export the calendar and import that tree"
            )

        content = body.get("body")
        if not (content and content.get("content")):
            body.pop("body", None)
        else:
            # Graph is case-insensitive here (measured); ``HTML``/``Text`` is what an import
            # has always sent, so the model's ``html`` is re-cased rather than the wire moving
            # silently.
            content["contentType"] = "HTML" if str(content.get("contentType")).lower() == "html" else "Text"
        # ``status`` is the attendee's own reply, which Exchange assigns: an import sends the
        # people, not the answers. Dropped here until a live create probe says otherwise.
        for attendee in body.get("attendees", ()):
            attendee.pop("status", None)
        if getattr(options, "use_transaction_ids", False):
            body["transactionId"] = self.transaction_id
        return body

    def dropped_attendees(self, options: CalendarImportOptions | None = None) -> int:
        """How many attendee entries the import leaves out, and so does not invite.

        Creating an event with attendees makes Exchange mail every one of them (measured),
        which is why replaying the list is opt-in; the count is what the run reports so the
        omission is a number rather than a silence.
        """
        options = self.options_class() if options is None else options
        if "attendees" not in withheld(options):
            return 0
        # Counted off the envelope: an attendee's address is a nested client value, and the
        # question here is only whether it has one.
        attendees = self._written(("attendees",)) or ()
        return sum(1 for attendee in attendees if (attendee.get("emailAddress") or {}).get("address"))

    @property
    def dedup_key(self) -> Tuple[str, Optional[str], Optional[str]]:
        """The key a target matches an existing event on: subject and start.

        A created event comes back with ``iCalUId: null`` and a fresh Graph id, so neither
        of the source's identities survives the import — subject plus wall clock (and the
        zone it is in) is what is left to recognise a re-run's own work by.
        """
        start = self.event.start
        moment = start.to_json(COMPARABLE) if start else {}
        return (str(self.event.subject or ""), moment.get("dateTime"), moment.get("timeZone"))

    @property
    def transaction_id(self) -> str:
        """A deterministic ``transactionId`` for an exported event: two runs collide, they do not both write."""
        return "mig-" + hashlib.sha1((self.source_id or self.dest_path).encode("utf-8")).hexdigest()[:32]


__all__ = [
    "EVENT_COLUMNS",
    "LEGACY_KEYS",
    "MAX_LINE_OCTETS",
    "CalendarExportOptions",
    "CalendarImportOptions",
    "EventRecord",
]
