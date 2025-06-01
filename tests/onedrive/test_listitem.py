from office365.onedrive.listitems.list_item import ListItem
from office365.onedrive.lists.list import List
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name, test_team_site_url
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestListItem(GraphTestCase):
    """"""

    target_list = None  # type: List
    target_item = None  # type: ListItem

    @classmethod
    def setUpClass(cls):
        super(TestListItem, cls).setUpClass()
        site = cls.client.sites.get_by_url(test_team_site_url)
        cls.target_list = site.lists.add(
            create_unique_name("Orders"), ListTemplateType.genericList
        ).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_list.delete_object().execute_query()

    @requires_delegated_permission("Sites.ReadWrite.All")
    def test1_create_item(self):
        result = self.target_list.items.add(Title="First Order").execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_item = result

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test2_list_items(self):
        result = self.target_list.items.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test3_get_item(self):
        item = self.__class__.target_item
        result = self.target_list.items[item.id].get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test4_get_column_values(self):
        item = self.__class__.target_item
        result = item.fields.select(["Title"]).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Sites.ReadWrite.All")
    def test5_update_item(self):
        item = self.__class__.target_item
        item.set_property("Title", "Updated title").update().execute_query()

    @requires_delegated_permission("Sites.ReadWrite.All")
    def test6_delete_item(self):
        item = self.__class__.target_item
        item.delete_object().execute_query()
