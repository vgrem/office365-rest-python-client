"""Tests for SharePoint client-side components (web parts, full-page applications)."""

from __future__ import annotations

from office365.sharepoint.publishing.pages.service import SitePageService

from tests.sharepoint.sharepoint_case import SPTestCase


class TestClientSideComponent(SPTestCase):
    """Tests for SharePoint client-side component operations."""

    def test_01_get_all_client_side_components(self):
        """Get all client-side components for the web."""
        result = self.client.web.get_all_client_side_components().execute_query()
        self.assertIsNotNone(result.value)

    def test_02_get_client_side_web_parts(self):
        """Get client-side web parts for the web."""
        result = self.client.web.get_client_side_web_parts().execute_query()
        self.assertIsNotNone(result.value)

    def test_03_get_available_full_page_applications(self):
        """Get available full-page applications."""
        result = SitePageService.get_available_full_page_applications(self.client).execute_query()
        self.assertIsNotNone(result.value)

    def test_04_list_client_web_parts(self):
        """List client-side web parts."""
        result = self.client.web.client_web_parts.get().execute_query()
        self.assertIsNotNone(result.resource_path)
