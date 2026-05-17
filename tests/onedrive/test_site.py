from office365.onedrive.sites.site import Site
from tests import test_team_site_url
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestSite(GraphTestCase):
    """OneDrive specific test case base class"""

    test_site: Site = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_site = cls.client.sites.root
        cls.followed_sites_count = None
        assert cls.test_site.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test1_get_root_site(self):
        result = self.client.sites.root.get().execute_query()
        assert result.id is not None

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test2_get_site_by_path(self):
        result = self.client.sites.get_by_path("/sites/team").execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test3_get_site_by_url(self):
        result = self.client.sites.get_by_url(test_team_site_url).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission(
        "Files.Read",
        "Files.ReadWrite",
        "Files.Read.All",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
    )
    def test4_get_activities_by_interval(self):
        col = self.test_site.get_activities_by_interval().execute_query()
        self.assertIsNotNone(col)

    @requires_delegated_permission("Sites.ReadWrite.All")
    def test5_follow(self):
        self.client.me.follow_site(self.test_site).execute_query()

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test6_list_followed_sites(self):
        result = self.client.me.followed_sites.get().execute_query()
        self.followed_sites_count = len(result)
        self.assertGreaterEqual(len(result), 1, "No followed sites were returned")

    @requires_delegated_permission("Sites.ReadWrite.All")
    def test7_unfollow(self):
        self.client.me.unfollow_site(self.test_site).execute_query()

    @requires_delegated_permission(
        "Sites.Read.All",
        "Sites.FullControl.All",
        "Sites.Manage.All",
        "Sites.ReadWrite.All",
    )
    def test9_get_operations(self):
        result = self.test_site.operations.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_10_get_analytics(self):
        result = self.test_site.analytics.last_seven_days.get().execute_query()
        self.assertIsNotNone(result.resource_path)
