"""Tests for Microsoft Graph OneNote Pages API."""

from typing import Optional

from office365.onenote.pages.page import OnenotePage
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestPage(GraphDelegatedTestCase):
    """Tests for OneNote pages."""

    target_page: Optional[OnenotePage] = None

    @requires_delegated_permission_or_role(
        "Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All", roles=["Global Administrator"]
    )
    def test1_create_page(self):
        """Create a new OneNote page."""

    @requires_delegated_permission_or_role(
        "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", roles=["Global Administrator"]
    )
    def test2_list_pages(self):
        """List OneNote pages from the first section."""
        sections = self.client.me.onenote.sections.top(1).get().execute_query()
        assert len(sections) > 0
        my_pages = sections[0].pages.get().top(10).execute_query()
        self.assertIsNotNone(my_pages.resource_path)
