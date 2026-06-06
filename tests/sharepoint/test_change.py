"""Tests for SharePoint change tracking (web, site, and list item changes)."""

from __future__ import annotations

from office365.sharepoint.changes.collection import ChangeCollection
from office365.sharepoint.changes.log_item_query import ChangeLogItemQuery

from tests.sharepoint.sharepoint_case import SPTestCase


class TestChange(SPTestCase):
    """Tests for SharePoint change tracking operations."""

    def test_01_get_web_changes(self):
        """Get changes for the root web."""
        result = self.client.site.root_web.get_changes().execute_query()
        self.assertIsInstance(result, ChangeCollection)

    def test_02_get_site_changes(self):
        """Get changes for the site."""
        result = self.client.site.get_changes().execute_query()
        self.assertIsInstance(result, ChangeCollection)

    def test_03_get_list_item_changes_since_token(self):
        """Get list item changes since a change token."""
        target_list = self.client.site.root_web.default_document_library()
        query = ChangeLogItemQuery(RowLimit="100")
        result = target_list.get_list_item_changes_since_token(query).execute_query()
        self.assertIsNotNone(result.value)
