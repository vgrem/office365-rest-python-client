from __future__ import annotations

from office365.sharepoint.publishing.pages.collection import SitePageCollection
from office365.sharepoint.publishing.pages.page import SitePage

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSitePages(SPTestCase):
    target_page: SitePage | None = None

    def test1_create_draft_page(self):
        page_title = create_unique_name("Site Page ")
        page = self.client.site_pages.create_page(page_title, "Site Page.aspx").execute_query()
        self.assertIsNotNone(page.resource_path)
        type(self).target_page = page

    def test2_list_site_pages(self):
        result = self.client.site_pages.pages.get().execute_query()
        self.assertIsInstance(result, SitePageCollection)
        self.assertIsNotNone(result.resource_path)

    def test3_publish_site_page(self):
        assert self.target_page is not None
        page = self.target_page
        page.publish().execute_query()
        self.assertIsNotNone(page.first_published)

    def test5_delete_site_page(self):
        assert self.target_page is not None
        page = self.target_page
        page.delete_object().execute_query()
