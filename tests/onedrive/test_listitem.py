from typing import Optional

from office365.onedrive.listitems.list_item import ListItem
from office365.onedrive.lists.list import List
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name, test_team_site_url
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestListItem(GraphDelegatedTestCase):
    """"""

    target_list: Optional[List] = None
    target_item: Optional[ListItem] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        site = cls.client.sites.get_by_url(test_team_site_url)
        cls.target_list = site.lists.add(create_unique_name("Orders"), ListTemplateType.genericList).execute_query()

    @classmethod
    def tearDownClass(cls):
        assert cls.target_list is not None
        cls.target_list.delete_object().execute_query()

    @requires_delegated("Sites.ReadWrite.All", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test1_create_item(self):
        """Create a list item"""
        assert self.target_list is not None
        result = self.target_list.items.add(Title="First Order").execute_query()
        assert result.resource_path is not None
        TestListItem.target_item = result

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test2_list_items(self):
        """List all items in the target list"""
        assert self.target_list is not None
        result = self.target_list.items.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test3_get_item(self):
        """Get a specific list item by ID"""
        item = TestListItem.target_item
        assert item is not None
        assert self.target_list is not None
        assert item.id is not None
        result = self.target_list.items[item.id].get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test4_get_column_values(self):
        """Get column values of a list item"""
        item = TestListItem.target_item
        assert item is not None
        result = item.fields.select(["Title"]).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.ReadWrite.All", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test5_update_item(self):
        """Update a list item"""
        item = TestListItem.target_item
        assert item is not None
        item.set_property("Title", "Updated title").update().execute_query()

    @requires_delegated("Sites.ReadWrite.All", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test6_delete_item(self):
        """Delete a list item"""
        item = TestListItem.target_item
        assert item is not None
        item.delete_object().execute_query()
