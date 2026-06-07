"""Tests for SharePoint site pages including creation, publishing, and deletion."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.publishing.pages.collection import SitePageCollection
from office365.sharepoint.publishing.pages.page import SitePage

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSitePages(SPTestCase):
    """Test SharePoint site pages features."""

    target_page: ClassVar[Optional[SitePage]] = None

    def test_01_create_draft_page(self):
        """Create a draft site page."""
        page_title = create_unique_name("Site Page ")
        page = self.client.site_pages.create_page(page_title, "Site Page.aspx").execute_query()
        self.assertIsNotNone(page.resource_path)
        TestSitePages.target_page = page

    def test_02_list_site_pages(self):
        """List all site pages."""
        result = self.client.site_pages.pages.get().execute_query()
        self.assertIsInstance(result, SitePageCollection)
        self.assertIsNotNone(result.resource_path)

    def test_03_publish_site_page(self):
        """Publish a site page."""
        target_page = TestSitePages.target_page
        if not target_page:
            self.skipTest("No target page from previous test")
        target_page.publish().execute_query()
        self.assertIsNotNone(target_page.first_published)

    def test_04_delete_site_page(self):
        """Delete the created site page."""
        target_page = TestSitePages.target_page
        if not target_page:
            self.skipTest("No target page from previous test")
        target_page.delete_object().execute_query()
