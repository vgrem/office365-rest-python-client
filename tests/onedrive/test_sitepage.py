from typing import Optional

from office365.onedrive.sitepages.site_page import SitePage
from tests import create_unique_name, test_team_site_url
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSitePage(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    target_page: Optional[SitePage] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_site = cls.client.sites.get_by_url(test_team_site_url)
        cls.page_name = create_unique_name("Test Page")
        cls.pages_list = cls.test_site.lists.get_by_name("Site Pages")

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test1_create_site_page(self):
        """Create a site page"""
        result = self.test_site.pages.add(self.page_name).execute_query()
        assert result.resource_path is not None
        TestSitePage.target_page = result

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test2_get_site_page(self):
        """Get a site page by ID"""
        page = TestSitePage.target_page
        assert page is not None
        result = page.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test3_get_item_by_name(self):
        """Get a page list item by name"""
        result = self.pages_list.items.get_by_name("Home.aspx").execute_query()
        assert result.resource_path is not None
        TestSitePage.target_item = result

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test4_checkin_site_page(self):
        """Check in a site page"""
        page = TestSitePage.target_page
        assert page is not None
        result = page.checkin("Initial version").execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test5_get_site_page_pub_state(self):
        """Get the publishing state of a site page"""
        page = TestSitePage.target_page
        assert page is not None
        result = page.get().select(["publishingState"]).execute_query()
        self.assertIsNotNone(result.publishing_state.level)

    # def test6_publish_site_page(self):
    #    page = self.__class__.target_page
    #    result = page.publish().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test7_list_site_pages(self):
        """List all site pages"""
        result = self.test_site.pages.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test8_get_site_page_by_name(self):
    #    result = self.test_site.pages.get_by_name(self.page_name).execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test9_get_site_page_by_title(self):
    #    page = self.__class__.target_page
    #    result = self.test_site.pages.get_by_title(page.title).execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test_10_get_web_parts_by_position(self):
    #    page = self.__class__.target_page
    #    result = page.get_web_parts_by_position().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test_11_delete_site_page(self):
        """Delete a site page"""
        page = TestSitePage.target_page
        assert page is not None
        page.delete_object().execute_query()

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test_12_get_site_page_list(self):
        """Get the Site Pages list"""
        result = self.test_site.lists.get_by_name("Site Pages").get().execute_query()
        self.assertIsNotNone(result.resource_path)
