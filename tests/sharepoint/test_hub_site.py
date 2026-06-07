from __future__ import annotations

from typing import ClassVar

from office365.sharepoint.portal.hub_sites_utility import SPHubSitesUtility

from tests.sharepoint.sharepoint_case import SPTestCase


class TestHubSite(SPTestCase):
    """Hub site management tests"""

    is_hub_site: ClassVar[bool] = False

    @classmethod
    def setUpClass(cls):
        super(TestHubSite, cls).setUpClass()
        cls.target_site = cls.client.site.get().execute_query()
        cls.is_hub_site = cls.target_site.is_hub_site or cls.target_site.hub_site_id is not None

    def test_01_register_hub_site(self):
        """Register the site as a hub site"""
        if self.is_hub_site:
            self.skipTest("This site is currently associated with a HubSite")
        site = self.target_site.register_hub_site().get().execute_query()
        self.assertTrue(site.is_hub_site)

    def test_02_get_hub_sites(self):
        """Get all hub sites"""
        result = SPHubSitesUtility(self.client).get_hub_sites().execute_query()
        self.assertGreater(len(result), 0)

    def test_03_unregister_hub_site(self):
        """Unregister the hub site"""
        if self.is_hub_site:
            self.skipTest("This site is not a HubSite")
        site = self.target_site.unregister_hub_site().get().execute_query()
        self.assertFalse(site.is_hub_site)
