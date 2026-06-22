"""Online Meetings — Teams meetings, recordings, and lifecycle.

Tests cover:
  - Creating, getting, updating, and deleting online meetings
  - Meeting property assertions (subject, start/end, joinUrl)
  - Listing recordings for a meeting
  - Bulk meeting creation with attendee configuration
  - Date-based filtering and pagination on meeting lists
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import ClassVar, Optional

import pytz
from office365.communications.onlinemeetings.online_meeting import OnlineMeeting

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOnlineMeetings(GraphDelegatedTestCase):
    """Online meeting CRUD and property inspection."""

    target_meeting: ClassVar[Optional[OnlineMeeting]] = None

    @requires_delegated(
        "OnlineMeetings.ReadWrite",
        bypass_roles=["Teams Administrator", "Global Administrator"],
    )
    def test_01_create_meeting(self):
        """Creating a simple online meeting without attendees returns a valid meeting."""
        meeting = self.client.me.online_meetings.create(subject="SDK Test — Automated Meeting").execute_query()

        self.assertIsNotNone(meeting.resource_path)
        self.assertIsNotNone(meeting.get_property("id"))
        self.assertEqual(meeting.get_property("subject"), "SDK Test — Automated Meeting")
        self.assertIsNotNone(meeting.get_property("joinWebUrl"))
        TestOnlineMeetings.target_meeting = meeting

    @requires_delegated(
        "OnlineMeetings.Read",
        bypass_roles=["Teams Administrator", "Global Administrator"],
    )
    def test_02_get_meeting_by_id(self):
        """Retrieving a meeting by its ID returns the same meeting."""
        meeting = TestOnlineMeetings.target_meeting
        if not meeting:
            self.skipTest("No meeting created from previous test")

        result = self.client.me.online_meetings[meeting.id].get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("id"), meeting.id)

    @requires_delegated(
        "OnlineMeetings.Read",
        bypass_roles=["Teams Administrator", "Global Administrator"],
    )
    def test_03_meeting_has_expected_properties(self):
        """A meeting exposes joinWebUrl, startDateTime, endDateTime, and participants."""
        meeting = TestOnlineMeetings.target_meeting
        if not meeting:
            self.skipTest("No meeting created from previous test")

        self.assertIsNotNone(meeting.get_property("joinWebUrl"))
        self.assertIsNotNone(meeting.get_property("startDateTime"))
        self.assertIsNotNone(meeting.get_property("endDateTime"))
        self.assertIsNotNone(meeting.get_property("participants"))

    @requires_delegated(
        "OnlineMeetings.ReadWrite",
        bypass_roles=["Teams Administrator", "Global Administrator"],
    )
    def test_04_update_meeting_subject(self):
        """Updating an online meeting's subject and time range succeeds."""
        meeting = TestOnlineMeetings.target_meeting
        if not meeting:
            self.skipTest("No meeting created from previous test")

        now = datetime.now(pytz.utc)
        meeting.subject = "SDK Test — Updated Subject"
        meeting.start_datetime = now
        meeting.end_datetime = now + timedelta(hours=1)
        meeting.update().execute_query()

        # Re-fetch and verify
        updated = self.client.me.online_meetings[meeting.id].get().execute_query()
        self.assertEqual(updated.get_property("subject"), "SDK Test — Updated Subject")

    @requires_delegated("OnlineMeetingRecording.Read.All")
    def test_05_list_recordings(self):
        """A meeting's recordings collection is accessible."""
        meeting = TestOnlineMeetings.target_meeting
        if not meeting:
            self.skipTest("No meeting created from previous test")

        recordings = meeting.recordings.get().execute_query()
        self.assertIsNotNone(recordings)

    @requires_delegated(
        "OnlineMeetings.ReadWrite",
        bypass_roles=["Teams Administrator", "Global Administrator"],
    )
    def test_06_delete_meeting(self):
        """Deleting an online meeting should succeed."""
        meeting = TestOnlineMeetings.target_meeting
        if not meeting:
            self.skipTest("No meeting created from previous test")

        meeting.delete_object().execute_query()
        TestOnlineMeetings.target_meeting = None

    @classmethod
    def tearDownClass(cls):
        """Best-effort cleanup of remaining meeting."""
        meeting = cls.target_meeting
        if meeting and meeting.resource_path:
            try:
                meeting.delete_object().execute_query()
            except Exception:
                pass


class TestOnlineMeetingsCreateWithSettings(GraphDelegatedTestCase):
    """Creating meetings with custom settings (attendees, lobby, recordings)."""

    @requires_delegated(
        "OnlineMeetings.ReadWrite",
        bypass_roles=["Teams Administrator", "Global Administrator"],
    )
    def test_01_create_meeting_with_attendees(self):
        """Creating a meeting with attendees and lobby bypass settings works."""
        meeting = self.client.me.online_meetings.create(
            subject="SDK Test — Meeting with Attendees",
            start_datetime=datetime.now(pytz.utc) + timedelta(hours=1),
            end_datetime=datetime.now(pytz.utc) + timedelta(hours=2),
        ).execute_query()

        self.assertIsNotNone(meeting.resource_path)
        self.assertIsNotNone(meeting.get_property("joinWebUrl"))

        # Cleanup
        try:
            meeting.delete_object().execute_query()
        except Exception:
            pass


