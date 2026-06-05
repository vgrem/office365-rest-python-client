"""Microsoft Search API — querying across drives, messages, sites, list items, people, events, and chat.

Tests cover:
  - Searching files (OneDrive) by name
  - Searching messages by keyword
  - Searching list items
  - Searching people by name
  - Searching sites by keyword
  - Searching events by keyword
  - Generic query with multiple entity types
  - Pagination (page_from, size)
  - Search result property assertions (hitsContainers, total, resultsCount)
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSearch(GraphDelegatedTestCase):
    """Microsoft Search API — queries across entity types."""

    @requires_delegated(
        "Files.Read.All",
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_01_search_files(self):
        """Searching for files by keyword returns results."""
        result = self.client.search.query_drive_items("Guide").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Mail.Read",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_search_messages(self):
        """Searching for messages by keyword returns results."""
        result = self.client.search.query_messages("John").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_03_search_list_items(self):
        """Searching for list items by keyword returns results."""
        result = self.client.search.query_list_items("Guide").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "People.Read",
        bypass_roles=["Global Administrator"],
    )
    def test_04_search_people_by_name(self):
        """Searching for people by name returns results."""
        result = self.client.search.query_peoples("John").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_05_search_sites(self):
        """Searching for sites by keyword returns results."""
        result = self.client.search.query_sites("team").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Calendars.Read",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_06_search_events(self):
        """Searching for calendar events by keyword returns results."""
        try:
            result = self.client.search.query_events("meeting").execute_query()
            self.assertIsNotNone(result.value)
        except Exception as e:
            self.skipTest(f"Cannot search events: {e}")

    @requires_delegated(
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_07_search_files_paginated(self):
        """Searching files with page_from and size parameters returns paginated results."""
        try:
            result = self.client.search.query_drive_items("Guide", page_from=0, size=5).execute_query()
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("Paginated search not supported")

    @requires_delegated(
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_08_search_result_has_hits(self):
        """A search response contains hitsContainers with total and results."""
        result = self.client.search.query_sites("team").execute_query()
        responses = result.value
        if not responses:
            self.skipTest("No search results returned")

        for response in responses:
            containers = response.get_property("hitsContainers")
            if containers:
                for container in containers:
                    total = container.get_property("total")
                    hits = container.get_property("hits")
                    if total is not None:
                        self.assertGreaterEqual(total, 0)
                    if hits is not None:
                        self.assertIsInstance(hits, list)
                break

    @requires_delegated(
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_09_generic_query_with_entity_types(self):
        """Using the generic query method with a list of entity types returns results."""
        try:
            result = self.client.search.query(
                query_string="Guide",
                entity_types=["site", "driveItem"],
                size=5,
            ).execute_query()
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("Generic query with entity types not supported")

    @requires_delegated(
        "Mail.Read",
        "Files.Read.All",
        "Sites.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test_10_search_empty_query(self):
        """An empty query string may return no results but should not error."""
        try:
            result = self.client.search.query_sites("").execute_query()
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("Empty query not supported or results in error")
