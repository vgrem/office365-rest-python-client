from office365.onedrive.columns.definition import ColumnDefinition
from office365.onedrive.lists.list import List
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.graph_case import GraphTestCase


class TestList(GraphTestCase):
    """OneDrive specific test case base class"""

    target_list: List = None
    target_column: ColumnDefinition = None
    list_name = create_unique_name("Documents")

    @classmethod
    def setUpClass(cls):
        super(TestList, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    def test1_create_list(self):
        result = self.client.sites.root.lists.add(self.list_name, ListTemplateType.documentLibrary).execute_query()
        self.__class__.target_list = result

    def test2_get_list(self):
        target_list = self.client.sites.root.lists[self.list_name].get().execute_query()
        self.assertIsNotNone(target_list.resource_path)

    def test3_get_list_items(self):
        result = self.target_list.items.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test4_get_list_columns(self):
        result = self.target_list.columns.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test5_create_list_column(self):
        column_name = create_unique_name("Text")
        result = self.target_list.columns.add_text(column_name).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_column = result

    def test6_delete_list_column(self):
        column_to_del = self.__class__.target_column
        column_to_del.delete_object().execute_query()

    def test7_delete_list(self):
        self.__class__.target_list.delete_object().execute_query()

    def test8_get_pages_list(self):
        result = self.client.sites.root.lists.get_by_name("Site Pages").get().execute_query()
        self.assertIsNotNone(result.resource_path)
