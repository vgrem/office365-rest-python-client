"""Calendar adapters — a Graph calendar as a source, an ICS tree as a target, and back.

Export a calendar::

    from office365.migration import MigrationJob
    from office365.migration.outlook import CalendarExportOptions, CalendarSource, IcsExportTarget

    calendar = client.me.calendar.get().execute_query()
    job = MigrationJob(CalendarSource(calendar), IcsExportTarget("./calendar-export"))
    job.plan()
    job.run()
    print(job.verify().summary())

Import it into another calendar::

    from office365.migration.outlook import CalendarImportOptions, CalendarTarget, IcsTreeSource

    options = CalendarImportOptions()
    target = client.me.calendars.add(name="Imported").execute_query()
    job = MigrationJob(IcsTreeSource("./calendar-export", options), CalendarTarget(target, options))
    job.plan()
    job.run()
    print(job.verify().summary())

Pass the *same* options object to both sides of an import: the source computes the
content digest of what the target promises to restore.

Export layout (the same convention the mail export uses)::

    <root>/<calendar>/<YYYY-MM-DD>_<subject-slug>_<id-digest>.ics   iCalendar document
    <root>/<calendar>/<same stem>.json                              sidecar record
    <root>/manifest.jsonl                                           one sidecar per line

One calendar per source: Graph exposes each calendar as its own event collection,
so a mailbox with several calendars is a job per calendar (or a loop), which also
keeps each export directory self-describing.

Six honest limits, all measured against Exchange:

* A recurring event is exported **once**, as its series master (``RRULE`` in the
  ``.ics``, ``recurrence`` in the sidecar); the individual occurrences are not
  separate items, because importing them would duplicate the series.
* Cancelled events are tombstones, skipped by default
  (``CalendarExportOptions.include_cancelled``): replaying one as a live meeting
  would be worse than losing the record of the cancellation.
* An ``.ics`` is a courtesy for other clients. Everything is also in the sidecar,
  which is what an import reads — iCalendar cannot carry Graph's recurrence object,
  the online-meeting provider, or the sensitivity/importance pair without loss.
* Attendees are **not re-added by default**: creating an event with attendees makes
  Exchange mail an invitation to each of them, so a historical import would spam
  people with meetings they already had. ``CalendarImportOptions.restore_attendees``
  turns it on, and the run reports how many entries were left out.
* Exchange assigns the meeting metadata on create — ``iCalUId``, the organizer,
  attendee responses, ``created``/``modified`` — so those cannot be restored, and
  the imported event is organised by the importing mailbox.
* The body is re-serialized (an HTML body gains Exchange's ``<head>``/``<style>``
  wrapper), which is why an import is verified by an event digest rather than by
  bytes.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from office365.migration.adapters import DataTarget, MigrationProgress, checksum
from office365.migration.base import MigrationItem
from office365.migration.outlook.adapters import ServiceSource, SidecarTreeSource, SidecarTreeTarget
from office365.migration.outlook.calendar_models import CalendarExportOptions, CalendarImportOptions, EventRecord
from office365.migration.outlook.fidelity import CALENDAR_EXPORT_DIMENSIONS, CALENDAR_IMPORT_DIMENSIONS
from office365.migration.outlook.records import slug
from office365.outlook.calendar.calendar import Calendar
from office365.outlook.calendar.events.event import Event
from office365.outlook.mail.messages.eventtype import EventType
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.http.prefer import prefer_outlook_timezone
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.operations import emit_progress
from office365.runtime.queries.create_entity import CreateEntityQuery

#: The narrow read an import uses to recognise its own work: identity, name, and the
#: wall clock the key is built from. Spelled through the model, so a rename cannot
#: leave it stale — and deliberately narrower than ``EventRecord.columns``, because this
#: one runs per item during a dedupe pass.
_EXISTING_COLUMNS = [Event.odata_name(attr) for attr in ("id", "subject", "start", "ical_uid")]

#: Graph's error code for a reused ``transactionId`` (a concurrent run got there first).
_DUPLICATE_TRANSACTION = "ErrorDuplicateTransactionId"


class CalendarSource(ServiceSource[Event]):
    """Enumerates one Graph calendar as one item per event.

    Each item carries its envelope in ``metadata``, so the export's index is written
    from the manifest itself — no second pass over the calendar.
    """

    #: What a calendar export preserves; see ``outlook.fidelity``.
    fidelity_dimensions = CALENDAR_EXPORT_DIMENSIONS

    def __init__(self, calendar: Calendar, options: CalendarExportOptions | None = None) -> None:
        super().__init__()
        self._calendar = calendar
        self._options = options or CalendarExportOptions()

    def label(self) -> str:
        name = self._options.root_name or getattr(self._calendar, "name", None) or self._calendar.id
        return f"calendar:{name}"

    def list_items(self, progress: MigrationProgress = None) -> list[MigrationItem]:
        root = self._options.root_name or slug(getattr(self._calendar, "name", None)) or "calendar"
        display = getattr(self._calendar, "name", None) or root
        items: list[MigrationItem] = []
        for event in self._calendar.events.select(list(EventRecord.columns)).get_all().execute_query():
            if not self._include(event):
                continue
            item = self._item(event, root, display)
            self._remember(item, event)
            items.append(item)
            emit_progress(progress, done=len(items), stage="planning", items=[item])
        self._enumerated = True
        return items

    def _include(self, event: Event) -> bool:
        """Whether an event is exported on its own (a series master, not an instance).

        An event that is neither a single instance nor a series master is an occurrence or
        an exception of a series, which the series already carries.
        """
        if event.is_cancelled and not self._options.include_cancelled:
            return False
        if event.type_ in (EventType.singleInstance, EventType.seriesMaster):
            return True
        return self._options.include_recurring_instances

    def _item(self, event: Event, path: str, display: str) -> MigrationItem:
        record = EventRecord.of(event, path, display, self._options.extra_properties)
        return MigrationItem(
            source_path=record.dest_path,
            dest_path=record.dest_path,
            # An event has no byte size until its ``.ics`` is rendered; ``read()`` fills it.
            size_bytes=0,
            item_type=EventRecord.item_type,
            modified=record.modified,
            created=record.created,
            source_id=record.source_id,
            metadata=record.to_json(),
        )

    def read(self, item: MigrationItem) -> bytes:
        """The event's ``.ics`` document, rendered from the record in ``metadata``."""
        data = EventRecord.from_json(item.metadata or {}).ics()
        item.size_bytes = len(data)
        return data

    def checksum(self, item: MigrationItem) -> str:
        return checksum(self.read(item))


class IcsExportTarget(SidecarTreeTarget):
    """Writes a portable ICS tree: one ``.ics`` plus one JSON sidecar per event."""

    fidelity_dimensions = CALENDAR_EXPORT_DIMENSIONS
    record = EventRecord


class IcsTreeSource(SidecarTreeSource[EventRecord]):
    """Reads an exported calendar tree back as migration items.

    The ``.ics`` is the payload (what another client would open); the JSON sidecar is the
    record the import replays, and it is **required** — an ``.ics`` alone cannot express
    Graph's recurrence object, and reading a calendar back out of iCalendar would invent an
    import that silently turns every series into a single meeting.
    """

    #: What a calendar import preserves; see ``outlook.fidelity``.
    fidelity_dimensions = CALENDAR_IMPORT_DIMENSIONS
    record = EventRecord
    sidecar_note = (
        "the sidecar is the import contract (the .ics cannot carry the recurrence object Exchange needs), so the"
        " tree has to come from a calendar export"
    )


class CalendarTarget(DataTarget):
    """Recreates exported events in a Graph calendar.

    The source of truth is the sidecar, not the ``.ics``: Graph's request body is
    posted verbatim (:meth:`EventRecord.payload`), because the typed helpers
    mangle the time zone and drop the ``transactionId``.
    """

    fidelity_dimensions = CALENDAR_IMPORT_DIMENSIONS

    def __init__(self, calendar: Calendar, options: CalendarImportOptions | None = None) -> None:
        self._calendar = calendar
        self._options = options or CalendarImportOptions()
        self._index: dict[tuple[str, str | None, str | None], list[Event]] | None = None
        self._claimed: dict[tuple[str, str | None, str | None], int] = {}
        self._present: dict[str, Event] = {}  # dest path -> created/found event
        self._attendees_dropped = 0
        #: Warnings a caller collects (the resolver convention).
        self.warnings: list[str] = []

    @property
    def calendar(self) -> Calendar:
        return self._calendar

    def label(self) -> str:
        name = getattr(self._calendar, "name", None) or self._calendar.id
        return f"calendar:{name}"

    # -- target contract -------------------------------------------------------

    def exists(self, item: MigrationItem) -> bool:
        """Whether an equal event is already in the target calendar.

        Matched on subject plus start, because nothing the source knows survives the
        create (a created event comes back with ``iCalUId: null`` and a fresh id).
        Duplicates *at the source* are honoured: the index keeps a list per key and
        each source item claims its own entry, so two same-titled events at the same
        hour are still imported twice.
        """
        if item.dest_path in self._present:
            return True
        key = EventRecord.from_json(item.metadata or {}).dedup_key
        candidates = self._target_index().get(key) or []
        claimed = self._claimed.get(key, 0)
        if claimed >= len(candidates):
            return False
        self._claimed[key] = claimed + 1
        self._present[item.dest_path] = candidates[claimed]
        return True

    def write(self, item: MigrationItem, payload: Any) -> None:
        """Create the event from its sidecar record.

        ``payload`` (the ``.ics`` bytes) is deliberately unused: Graph's create body is
        the record's fields, and re-parsing the iCalendar would lose the recurrence
        object the export preserved precisely so this could be exact.
        """
        if item.item_type != "event":
            raise ValueError(f"a calendar imports events, not {item.item_type!r} ({item.dest_path})")
        record = EventRecord.from_json(item.metadata or {})
        collection = self._calendar.events
        try:
            body = record.payload(self._options)
        except ValueError as e:
            raise ValueError(f"{item.dest_path}: {e}") from None
        event = collection.create_typed_object()
        collection.context.add_query(CreateEntityQuery(collection, body, event))
        try:
            collection.context.execute_query()
        except ClientRequestException as e:
            adopted = self._adopt_duplicate(e, item)
            if adopted is None:
                raise
            self._present[item.dest_path] = adopted
            return
        self._attendees_dropped += record.dropped_attendees(self._options)
        self._present[item.dest_path] = event
        key = record.dedup_key
        self._target_index().setdefault(key, []).append(event)
        self._claimed[key] = self._claimed.get(key, 0) + 1

    def list_paths(self) -> Iterable[str]:
        """The destination paths this target has created or recognised.

        A calendar cannot be enumerated back into export paths (the paths carry the
        source's date slug), so extras are not reported: the validator's presence pass
        covers what the plan expects, and the target-side extras are events the user
        already had.
        """
        return sorted(self._present)

    def checksum(self, item: MigrationItem) -> str:
        """Fingerprint of the event as the target calendar returns it.

        The re-read asks for the *source item's* timezone (``Prefer:
        outlook.timezone``): Exchange renders event times in the signed-in mailbox's
        own zone otherwise, so a migration into a mailbox set to another zone would
        report every event as a content mismatch while the instants were identical
        (measured: ``09:00 W. Europe`` reads back as ``07:00 UTC`` unasked).
        """
        event = self._present.get(item.dest_path)
        if event is None or not event.id:
            return ""
        read = self._calendar.events[event.id]
        read.select(list(EventRecord.columns)).get()
        zone = ((item.metadata or {}).get("start") or {}).get("timeZone")
        if zone:
            read.before_execute(_prefer_zone(zone))
        self._calendar.context.execute_query()
        return EventRecord.of(read).digest(self._options)

    def commit(self, options: Any = None) -> None:  # noqa: ARG002 — runner hook signature
        """Report once what the run deliberately did not restore."""
        if self._attendees_dropped:
            self.warnings.append(
                f"{self._attendees_dropped} attendee entries were not restored: re-adding them makes Exchange"
                " send an invitation to every attendee of every imported event (measured), so it is opt-in —"
                " pass CalendarImportOptions(restore_attendees=True) to replay them"
            )

    # -- helpers ---------------------------------------------------------------

    def _target_index(self) -> dict[tuple[str, str | None, str | None], list[Event]]:
        """The target calendar's events, grouped by the key an import recognises."""
        if self._index is None:
            index: dict[tuple[str, str | None, str | None], list[Event]] = {}
            for event in self._calendar.events.select(_EXISTING_COLUMNS).get_all().execute_query():
                index.setdefault(EventRecord.of(event).dedup_key, []).append(event)
            self._index = index
        return self._index

    def _adopt_duplicate(self, error: Exception, item: MigrationItem) -> Any:
        """The event a concurrent run created with our ``transactionId``, if any.

        The id is derived from the source event, so a collision means the interesting
        work is already done — adopting the event keeps the run idempotent instead of
        failing on a resume that overlapped another.
        """
        if _DUPLICATE_TRANSACTION not in str(error):
            return None
        self._index = None
        candidates = self._target_index().get(EventRecord.from_json(item.metadata or {}).dedup_key) or []
        return candidates[-1] if candidates else None


def _prefer_zone(zone: str) -> Callable[[RequestOptions], None]:
    """A ``before_execute`` hook that renders the read in ``zone``."""

    def handler(request: RequestOptions) -> None:
        prefer_outlook_timezone(request, zone)

    return handler


__all__ = ["CalendarSource", "CalendarTarget", "IcsExportTarget", "IcsTreeSource"]
