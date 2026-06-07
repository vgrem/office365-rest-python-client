from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestOrgNews(SPTestCase):
    """Organizational news tests"""

    def test_01_get_org_news(self):
        """Get organizational news"""
        result = self.client.org_news.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_02_sites_reference(self):
        """Get sites reference for organizational news"""
        result = self.client.org_news.sites_reference().execute_query()
        self.assertIsNotNone(result.value)
