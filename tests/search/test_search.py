"""Tests for Microsoft Search API."""

from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphTestCase


class TestSearchOneDrive(GraphTestCase):
    """Tests for Microsoft Search API across OneDrive, mail, and sites."""

    @requires_delegated_permission_or_role(
        "Files.Read.All",
        "Sites.Read.All",
        roles=["Global Administrator"],
    )
    def test1_search_files(self):
        """Search for files by name."""
        result = self.client.search.query_drive_items("Guide.docx").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role(
        "Mail.Read",
        roles=["Global Administrator"],
    )
    def test2_search_messages(self):
        """Search for messages by keyword."""
        result = self.client.search.query_messages("Jon Doe").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role(
        "Sites.Read.All",
        roles=["Global Administrator"],
    )
    def test3_search_list_items(self):
        """Search for list items by keyword."""
        result = self.client.search.query_list_items("Guide").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role(
        "People.Read",
        roles=["Global Administrator"],
    )
    def test4_search_people_by_name(self):
        """Search for people by name."""
        result = self.client.search.query_peoples("John").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role(
        "Sites.Read.All",
        roles=["Global Administrator"],
    )
    def test5_search_sites(self):
        """Search for sites by keyword."""
        result = self.client.search.query_sites("team").execute_query()
        self.assertIsNotNone(result.value)
