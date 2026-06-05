"""Site pages — creating, getting, checking in, publishing state, listing, deleting.

Tests cover:
  - Creating a site page
  - Getting a site page by ID
  - Getting a page list item by name
  - Checking in a site page
  - Getting site page publishing state
  - Listing all site pages
  - Deleting a site page
  - Getting the Site Pages list
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.onedrive.sitepages.site_page import SitePage

from tests import create_unique_name, test_team_site_url
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSitePage(GraphDelegatedTestCase):
    """Site page CRUD and publishing."""

    target_page: ClassVar[Optional[SitePage]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_site = cls.client.sites.get_by_url(test_team_site_url)
        cls.page_name = create_unique_name("Test Page")

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_create_site_page(self):
        """Creating a site page should succeed."""
        result = self.test_site.pages.add(self.page_name).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertIsNotNone(result.get_property("id"))
        TestSitePage.target_page = result

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_02_get_site_page(self):
        """Getting a site page by ID returns the same page."""
        page = TestSitePage.target_page
        if not page:
            self.skipTest("No page created from previous test")

        result = page.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_03_checkin_site_page(self):
        """Checking in a site page should succeed."""
        page = TestSitePage.target_page
        if not page:
            self.skipTest("No page created from previous test")

        result = page.checkin("Initial version").execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_04_get_publishing_state(self):
        """Getting the publishing state of a site page returns a level."""
        page = TestSitePage.target_page
        if not page:
            self.skipTest("No page created from previous test")

        result = page.get().select(["publishingState"]).execute_query()
        self.assertIsNotNone(result.get_property("publishingState"))

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_05_list_site_pages(self):
        """Listing all site pages with $top=10 returns a valid collection."""
        result = self.test_site.pages.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_06_delete_site_page(self):
        """Deleting a site page should succeed."""
        page = TestSitePage.target_page
        if not page:
            self.skipTest("No page created from previous test")

        page.delete_object().execute_query()
        TestSitePage.target_page = None

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_07_get_site_pages_list(self):
        """Getting the Site Pages list returns a valid list."""
        result = self.test_site.lists.get_by_name("Site Pages").get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @classmethod
    def tearDownClass(cls):
        page = cls.target_page
        if page and page.resource_path:
            try:
                page.delete_object().execute_query()
            except Exception:
                pass
