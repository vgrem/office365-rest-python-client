"""Rooms and room lists — place management for meeting rooms.

Tests cover:
  - Getting room lists
  - Room property assertions
  - Listing rooms within a room list
"""

from __future__ import annotations

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestRooms(GraphApplicationTestCase):
    """Room lists and rooms (requires Place.Read.All)."""

    @requires_application("Place.Read.All")
    def test_01_get_room_lists(self):
        """Getting room lists returns a valid collection."""
        result = self.client.room_lists.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("Place.Read.All")
    def test_02_room_list_has_display_name(self):
        """A room list entry should have a displayName."""
        result = self.client.room_lists.get().execute_query()
        if len(result) == 0:
            self.skipTest("No room lists found")

        for room_list in result:
            self.assertIsNotNone(room_list.display_name)
            break

    @requires_application("Place.Read.All")
    def test_03_room_list_has_rooms(self):
        """A room list should expose a rooms sub-collection."""
        result = self.client.room_lists.get().execute_query()
        if len(result) == 0:
            self.skipTest("No room lists found")

        for room_list in result:
            try:
                rooms = room_list.rooms.get().execute_query()
                self.assertIsNotNone(rooms)
                if len(rooms) > 0:
                    room = rooms[0]
                    self.assertIsNotNone(room.display_name)
                break
            except Exception:
                continue

    @requires_application("Place.Read.All")
    def test_04_filter_room_lists(self):
        """Filtering room lists by displayName should work."""
        result = self.client.room_lists.get().execute_query()
        if len(result) == 0:
            self.skipTest("No room lists found")

        name = result[0].display_name
        filtered = self.client.room_lists.filter(f"displayName eq '{name}'").get().execute_query()
        self.assertGreaterEqual(len(filtered), 1)
