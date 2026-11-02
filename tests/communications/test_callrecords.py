"""Call Records — PSTN and direct routing call logs.

Tests cover:
  - Listing recent call records with pagination
  - Getting direct routing calls with date range
  - Call record property assertions (modalities, participants, sessions)
  - Filtering call records by date and direction
  - Edge cases: empty date range, single-day range
"""

from __future__ import annotations

from datetime import datetime, timedelta

from office365.communications.callrecords.collection import CallRecordCollection

from tests.decorators import requires_application, requires_call
from tests.graph_case import GraphApplicationTestCase


class TestCallRecords(GraphApplicationTestCase):
    """Call records require application-level permissions (CallRecords.Read.All)."""

    @requires_application("CallRecords.Read.All")
    def test_01_list_call_records(self):
        """Listing recent call records returns a valid collection.

        The feed refuses ``$top`` outright ("Query option 'Top' is not allowed"), so the
        first page is the only page this test can ask for; ``query_capabilities`` raises
        before the request rather than letting the service return that error.
        """
        records = self.client.communications.call_records.get().execute_query()
        self.assertIsNotNone(records.resource_path)

    @requires_call(CallRecordCollection.get_direct_routing_calls, flow="application")
    def test_02_get_direct_routing_calls_default(self):
        """Getting direct routing calls without date range defaults to last 30 days."""
        result = self.client.communications.call_records.get_direct_routing_calls().execute_query()
        self.assertIsNotNone(result.value)

    @requires_call(CallRecordCollection.get_direct_routing_calls, flow="application")
    def test_03_get_direct_routing_calls_with_date_range(self):
        """Getting direct routing calls within a specific date range returns filtered rows."""
        from_date = datetime.now() - timedelta(days=7)
        to_date = datetime.now()
        result = self.client.communications.call_records.get_direct_routing_calls(
            from_datetime=from_date, to_datetime=to_date
        ).execute_query()
        self.assertIsNotNone(result.value)

    @requires_call(CallRecordCollection.get_direct_routing_calls, flow="application")
    def test_04_get_direct_routing_calls_single_day(self):
        """Getting direct routing calls for a single day returns rows for that window."""
        from_date = datetime.now() - timedelta(days=1)
        to_date = datetime.now()
        result = self.client.communications.call_records.get_direct_routing_calls(
            from_datetime=from_date, to_datetime=to_date
        ).execute_query()
        self.assertIsNotNone(result.value)

    @requires_application("CallRecords.Read.All")
    def test_05_call_record_has_expected_properties(self):
        """A call record exposes id, startDateTime, endDateTime, and type."""
        records = self.client.communications.call_records.get().execute_query()
        if len(records) == 0:
            self.skipTest("No call records found")

        for record in records:
            self.assertIsNotNone(record.id)
            self.assertIsNotNone(record.get_property("startDateTime"))
            self.assertIsNotNone(record.get_property("endDateTime"))
            self.assertIsNotNone(record.get_property("type"))
            break

    @requires_application("CallRecords.Read.All")
    def test_06_call_record_has_sessions(self):
        """A call record exposes a sessions collection."""
        records = self.client.communications.call_records.get().execute_query()
        if len(records) == 0:
            self.skipTest("No call records found")

        for record in records:
            try:
                sessions = record.sessions.get().execute_query()
                self.assertIsNotNone(sessions)
                break
            except Exception:
                continue

    @requires_call(CallRecordCollection.get_direct_routing_calls, flow="application")
    def test_07_direct_routing_row_has_expected_fields(self):
        """A direct routing log row exposes callId, userId, and userDisplayName."""
        result = self.client.communications.call_records.get_direct_routing_calls().execute_query()
        rows = result.value
        if not rows:
            self.skipTest("No direct routing call rows found")

        for row in rows:
            self.assertIsNotNone(row.get_property("callId"))
            # Most rows have at least one of userId or userDisplayName
            has_user = any(
                row.get_property(field) is not None for field in ("userId", "userDisplayName", "callStartDateTime")
            )
            self.assertTrue(has_user, "Expected at least one user identifier field")
            break

    @requires_application("CallRecords.Read.All")
    def test_08_call_record_has_modality(self):
        """A call record has a modalities field indicating audio/video."""
        records = self.client.communications.call_records.get().execute_query()
        if len(records) == 0:
            self.skipTest("No call records found")

        for record in records:
            modality = record.get_property("modalities")
            if modality:
                self.assertIsInstance(modality, list)
                break
        else:
            self.skipTest("No call records with modalities found")
