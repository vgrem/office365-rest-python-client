from office365.sharepoint.portal.hub_sites_utility import SPHubSitesUtility
from tests.sharepoint.sharepoint_case import SPTestCase


class TestHubSite(SPTestCase):
    is_hub_site = False

    @classmethod
    def setUpClass(cls):
        super(TestHubSite, cls).setUpClass()
        cls.target_site = cls.client.site.get().execute_query()
        cls.is_hub_site = (
            cls.target_site.is_hub_site or cls.target_site.hub_site_id is not None
        )

    def test1_register_hub_site(self):
        if self.is_hub_site:
            self.skipTest("This site is currently associated with a HubSite")
        site = self.target_site.register_hub_site().get().execute_query()
        self.assertTrue(site.is_hub_site)

    def test2_get_hub_sites(self):
        result = SPHubSitesUtility(self.client).get_hub_sites().execute_query()
        self.assertGreater(len(result), 0)

    def test3_unregister_hub_site(self):
        if self.is_hub_site:
            self.skipTest("This site is not a HubSite")
        site = self.target_site.unregister_hub_site().get().execute_query()
        self.assertFalse(site.is_hub_site)
