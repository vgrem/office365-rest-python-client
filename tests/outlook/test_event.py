"""Calendar Events — event CRUD, cancel, and multi-property inspection.

Tests cover:
  - Creating a calendar event with subject, body, start/end, and attendees
  - Listing events for the user
  - Updating an event subject
  - Cancelling an event (organizer only)
  - Deleting an event and verifying removal
  - Event property assertions (subject, body, attendees)
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import ClassVar, Optional

from office365.outlook.calendar.events.event import Event
from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.outlook.mail.recurrence_pattern import RecurrencePattern
from office365.outlook.mail.recurrence_range import RecurrenceRange
from office365.outlook.mail.recurrencepatterntype import RecurrencePatternType
from office365.outlook.mail.recurrencerangetype import RecurrenceRangeType

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookEvent(GraphDelegatedTestCase):
    """Event CRUD and lifecycle management."""

    target_event: ClassVar[Optional[Event]] = None

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_event(self):
        """Creating an event with subject, time, and attendees should succeed."""
        when = datetime.now() + timedelta(days=1)
        result = self.client.me.calendar.events.add(
            subject="Let's go for lunch",
            body="Does mid month work for you?",
            start=when,
            end=when + timedelta(hours=1),
            attendees=[test_user_principal_name],
        ).execute_query()
        self.assertIsNotNone(result.get_property("id"))
        self.assertEqual(result.get_property("subject"), "Let's go for lunch")
        TestOutlookEvent.target_event = result

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_list_events(self):
        """Listing events for the user returns at least one event."""
        result = self.client.me.events.get().execute_query()
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_event_has_expected_properties(self):
        """An event exposes subject, start, end, attendees, and organizer."""
        event = TestOutlookEvent.target_event
        if not event:
            self.skipTest("No event created from previous test")

        self.assertIsNotNone(event.get_property("subject"))
        self.assertIsNotNone(event.get_property("start"))
        self.assertIsNotNone(event.get_property("end"))
        self.assertIsNotNone(event.get_property("attendees"))
        self.assertIsNotNone(event.get_property("organizer"))

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_update_event_subject(self):
        """Updating an event's subject should persist."""
        event = TestOutlookEvent.target_event
        if not event:
            self.skipTest("No event created from previous test")

        event.subject = "Let's go for lunch (updated)"
        event.update().execute_query()
        assert event.id is not None
        updated = self.client.me.calendar.events[event.id].get().execute_query()
        self.assertEqual(updated.get_property("subject"), "Let's go for lunch (updated)")

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_cancel_event(self):
        """Cancelling an event with a comment should succeed (organizer only)."""
        event = TestOutlookEvent.target_event
        if not event:
            self.skipTest("No event created from previous test")

        event.cancel(comment="Cancelled: schedule conflict").execute_query()

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_06_delete_event(self):
        """Deleting an event should remove it from the user's events."""
        event = TestOutlookEvent.target_event
        if not event:
            self.skipTest("No event created from previous test")

        event_id = event.get_property("id")
        event.delete_object().execute_query()

        remaining = self.client.me.events.get().execute_query()
        matches = [e for e in remaining if e.id == event_id]
        self.assertEqual(len(matches), 0)
        TestOutlookEvent.target_event = None

    @requires_delegated(
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_07_create_recurring_event(self):
        """Creating a weekly recurring event with 4 occurrences should succeed."""
        when = datetime.now() + timedelta(days=1)
        result = self.client.me.calendar.events.add(
            subject="Weekly Standup",
            body="Team sync.",
            start=when,
            end=when + timedelta(hours=1),
        ).execute_query()
        self.assertIsNotNone(result.get_property("id"))

        # Set recurrence pattern after creation
        result.set_property(
            "recurrence",
            PatternedRecurrence(
                pattern=RecurrencePattern(
                    type=RecurrencePatternType.weekly.value,
                    interval=1,
                ),
                range=RecurrenceRange(
                    type=RecurrenceRangeType.numbered.value,
                    numberOfOccurrences=4,
                    startDate=when.date(),
                ),
            ),
        ).update().execute_query()

        # Re-fetch to verify recurrence persisted
        updated = self.client.me.calendar.events[result.id].get().execute_query()
        self.assertIsNotNone(updated.get_property("recurrence"))
        result.delete_object().execute_query()

    @classmethod
    def tearDownClass(cls):
        event = cls.target_event
        if event and event.resource_path:
            try:
                event.delete_object().execute_query()
            except Exception:
                pass
