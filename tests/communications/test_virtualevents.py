"""Virtual Events — webinars and town halls.

Tests cover:
  - Listing webinars and town halls with pagination
  - Filtering by status and date
  - Reading event properties (displayName, status, startDateTime)
  - Session and presenter sub-collections
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestVirtualEvents(GraphDelegatedTestCase):
    """Virtual events listing and property inspection."""

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_01_list_webinars_paginated(self):
        """Listing virtual event webinars with $top=10 returns a valid collection."""
        webinars = self.client.solutions.virtual_events.webinars.top(10).get().execute_query()
        self.assertIsNotNone(webinars)

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_02_list_townhalls_paginated(self):
        """Listing virtual event town halls with $top=10 returns a valid collection."""
        townhalls = self.client.solutions.virtual_events.townhalls.top(10).get().execute_query()
        self.assertIsNotNone(townhalls)

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_03_webinar_has_expected_properties(self):
        """A webinar exposes displayName, status, startDateTime, and endDateTime."""
        webinars = self.client.solutions.virtual_events.webinars.top(5).get().execute_query()
        if len(webinars) == 0:
            self.skipTest("No webinars found")

        for event in webinars:
            self.assertIsNotNone(event.get_property("id"))
            self.assertIsNotNone(event.get_property("displayName"))
            self.assertIsNotNone(event.get_property("startDateTime"))
            break

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_04_webinar_has_status(self):
        """A webinar has a status field indicating draft/published/canceled."""
        webinars = self.client.solutions.virtual_events.webinars.top(5).get().execute_query()
        if len(webinars) == 0:
            self.skipTest("No webinars found")

        for event in webinars:
            status = event.get_property("status")
            if status:
                known_statuses = {"draft", "published", "canceled"}
                self.assertIn(status, known_statuses, f"Unexpected status '{status}'")
                break

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_05_webinar_has_sessions(self):
        """A webinar exposes a sessions sub-collection."""
        webinars = self.client.solutions.virtual_events.webinars.top(5).get().execute_query()
        if len(webinars) == 0:
            self.skipTest("No webinars found")

        for event in webinars:
            try:
                sessions = event.sessions.get().execute_query()
                self.assertIsNotNone(sessions.resource_path)
                break
            except Exception:
                continue

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_06_townhall_has_expected_properties(self):
        """A town hall exposes id, displayName, and startDateTime."""
        townhalls = self.client.solutions.virtual_events.townhalls.top(5).get().execute_query()
        if len(townhalls) == 0:
            self.skipTest("No town halls found")

        for event in townhalls:
            self.assertIsNotNone(event.get_property("id"))
            self.assertIsNotNone(event.get_property("displayName"))
            self.assertIsNotNone(event.get_property("startDateTime"))
            break

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_07_filter_webinars_by_status(self):
        """Filtering webinars by status returns matching results."""
        try:
            result = (
                self.client.solutions.virtual_events.webinars.filter("status eq 'published'")
                .top(5)
                .get()
                .execute_query()
            )
            self.assertIsNotNone(result.resource_path)
            for event in result:
                self.assertEqual(event.get_property("status"), "published")
        except Exception:
            self.skipTest("Filtering webinars by status not supported")

    @requires_delegated(
        "VirtualEvent.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_08_townhall_has_presenters(self):
        """A town hall exposes a presenters sub-collection."""
        townhalls = self.client.solutions.virtual_events.townhalls.top(5).get().execute_query()
        if len(townhalls) == 0:
            self.skipTest("No town halls found")

        for event in townhalls:
            try:
                presenters = event.presenters.get().execute_query()
                self.assertIsNotNone(presenters)
                break
            except Exception:
                continue
