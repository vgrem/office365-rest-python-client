"""Tests for SharePoint change tracking (web, site, and list item changes)."""

from __future__ import annotations

from office365.sharepoint.changes.collection import ChangeCollection
from office365.sharepoint.changes.log_item_query import ChangeLogItemQuery
from office365.sharepoint.lists.list import List
from office365.sharepoint.sites.site import Site
from office365.sharepoint.webs.web import Web

from tests.decorators import requires_call
from tests.sharepoint.sharepoint_case import SPTestCase


class TestChange(SPTestCase):
    """Tests for SharePoint change tracking operations."""

    @requires_call(Web.get_changes, flow="application")
    def test_01_get_web_changes(self):
        """Get changes for the root web."""
        result = self.client.site.root_web.get_changes().execute_query()
        self.assertIsInstance(result, ChangeCollection)

    @requires_call(Site.get_changes, flow="application")
    def test_02_get_site_changes(self):
        """Get changes for the site."""
        result = self.client.site.get_changes().execute_query()
        self.assertIsInstance(result, ChangeCollection)

    @requires_call(List.get_list_item_changes_since_token, flow="application")
    def test_03_get_list_item_changes_since_token(self):
        """Get list item changes since a change token."""
        target_list = self.client.site.root_web.default_document_library()
        query = ChangeLogItemQuery(RowLimit="100")
        result = target_list.get_list_item_changes_since_token(query).execute_query()
        self.assertIsNotNone(result.value)
