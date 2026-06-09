from typing import Optional

from office365.onedrive.sites.site import Site
from tests import test_team_site_url
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSite(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    test_site: Optional[Site] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_site = cls.client.sites.root
        cls.followed_sites_count = None
        assert cls.test_site.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test1_get_root_site(self):
        """Get the root site"""
        result = self.client.sites.root.get().execute_query()
        assert result.id is not None

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test2_get_site_by_path(self):
        """Get a site by its server-relative path"""
        result = self.client.sites.get_by_path("/sites/project").execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test3_get_site_by_url(self):
        """Get a site by its absolute URL"""
        result = self.client.sites.get_by_url(test_team_site_url).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.Read",
        "Files.ReadWrite",
        "Files.Read.All",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test4_get_activities_by_interval(self):
        """Get activities for the site by time interval"""
        assert self.test_site is not None
        col = self.test_site.get_activities_by_interval().execute_query()
        self.assertIsNotNone(col)

    @requires_delegated("Sites.ReadWrite.All", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test5_follow(self):
        """Follow the test site"""
        assert self.test_site is not None
        self.client.me.follow_site(self.test_site).execute_query()

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test6_list_followed_sites(self):
        """List all followed sites"""
        result = self.client.me.followed_sites.get().execute_query()
        self.followed_sites_count = len(result)
        self.assertGreaterEqual(len(result), 1, "No followed sites were returned")

    @requires_delegated("Sites.ReadWrite.All", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test7_unfollow(self):
        """Unfollow the test site"""
        assert self.test_site is not None
        self.client.me.unfollow_site(self.test_site).execute_query()

    @requires_delegated(
        "Sites.Read.All",
        "Sites.FullControl.All",
        "Sites.Manage.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test9_get_operations(self):
        """Get site operations"""
        assert self.test_site is not None
        result = self.test_site.operations.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_10_get_analytics(self):
        """Get analytics for the test site"""
        assert self.test_site is not None
        result = self.test_site.analytics.last_seven_days.get().execute_query()
        self.assertIsNotNone(result.resource_path)
