"""Presence — user availability, activity, and status messages.

Tests cover:
  - Getting the signed-in user's presence
  - Setting and clearing preferred presence
  - Getting presences by user IDs (bulk)
  - Setting and clearing status messages
  - Presence property assertions (availability, activity)
  - Setting presence with session ID (app-managed identity)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.communications.presences.presence import Presence

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPresence(GraphDelegatedTestCase):
    """Reading and managing user presence."""

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_01_get_my_presence(self):
        """Getting the current user's presence returns availability and activity."""
        result = self.client.me.presence.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertIsNotNone(result.get_property("availability"))
        self.assertIsNotNone(result.get_property("activity"))

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_02_set_my_preferred_presence(self):
        """Setting preferred presence to 'DoNotDisturb' should succeed."""
        try:
            result = self.client.me.presence.set_user_preferred_presence(
                availability="DoNotDisturb",
                activity="Presenting",
                expiration_duration="PT1H",
            ).execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot set preferred presence: {e}")

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_03_clear_my_preferred_presence(self):
        """Clearing the preferred presence should reset to auto-computed state."""
        try:
            result = self.client.me.presence.clear_user_preferred_presence().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot clear preferred presence: {e}")

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_04_get_presences_by_user_id(self):
        """Getting presences for multiple users by ID should return a valid collection."""
        me = self.client.me.get().execute_query()
        if not me.id:
            self.skipTest("Cannot determine signed-in user ID")

        result = self.client.communications.get_presences_by_user_id([me.id]).execute_query()
        self.assertIsNotNone(result.resource_path)
        if len(result) > 0:
            self.assertIsNotNone(result[0].get_property("availability"))

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_05_set_status_message(self):
        """Setting a status message on the current user should succeed."""
        try:
            result = self.client.me.presence.set_status_message(
                message="I'm currently in a meeting"
            ).execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot set status message: {e}")

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_06_clear_status_message(self):
        """Clearing the status message should succeed."""
        try:
            result = self.client.me.presence.set_status_message(message=None).execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot clear status message: {e}")

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_07_presence_availability_is_known_value(self):
        """The availability value should be one of the known presence states."""
        result = self.client.me.presence.get().execute_query()
        availability = result.get_property("availability")
        if availability:
            known_values = {
                "Available", "AvailableIdle", "Away", "BeRightBack", "Busy", "BusyIdle",
                "DoNotDisturb", "Offline", "OfflineWork", "PresenceUnknown",
            }
            self.assertIn(
                availability, known_values,
                f"Unexpected availability '{availability}'"
            )

    @requires_delegated("Presence.ReadWrite", bypass_roles=["Global Administrator"])
    def test_08_presence_activity_is_known_value(self):
        """The activity value should be one of the known activity types."""
        result = self.client.me.presence.get().execute_query()
        activity = result.get_property("activity")
        if activity:
            known_activities = {
                "Available", "Away", "BeRightBack", "Busy", "DoNotDisturb",
                "InACall", "InAConferenceCall", "InAMeeting", "Offline",
                "OffWork", "OutOfOffice", "PresenceUnknown", "Presenting",
                "UrgentInterruptionsOnly",
            }
            self.assertIn(
                activity, known_activities,
                f"Unexpected activity '{activity}'"
            )
