from typing import Optional

from office365.onedrive.columns.definition import ColumnDefinition
from office365.onedrive.lists.list import List
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestList(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    target_list: Optional[List] = None
    target_column: Optional[ColumnDefinition] = None
    list_name = create_unique_name("Documents")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test1_create_list(self):
        """Create a list"""
        result = self.client.sites.root.lists.add(self.list_name, ListTemplateType.documentLibrary).execute_query()
        TestList.target_list = result

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test2_get_list(self):
        """Get a list by name"""
        target_list = self.client.sites.root.lists[self.list_name].get().execute_query()
        self.assertIsNotNone(target_list.resource_path)

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test3_get_list_items(self):
        """Get items from the target list"""
        assert TestList.target_list is not None
        result = TestList.target_list.items.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test4_get_list_columns(self):
        """Get columns from the target list"""
        assert TestList.target_list is not None
        result = TestList.target_list.columns.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test5_create_list_column(self):
        """Create a text column in the target list"""
        column_name = create_unique_name("Text")
        assert TestList.target_list is not None
        result = TestList.target_list.columns.add_text(column_name).execute_query()
        assert result.resource_path is not None
        TestList.target_column = result

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test6_delete_list_column(self):
        """Delete a column from the target list"""
        column_to_del = TestList.target_column
        assert column_to_del is not None
        column_to_del.delete_object().execute_query()

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test7_delete_list(self):
        """Delete the target list"""
        assert TestList.target_list is not None
        TestList.target_list.delete_object().execute_query()

    @requires_delegated_permission_or_role("Sites.Read.All", "Sites.ReadWrite.All", roles=["Global Administrator"])
    def test8_get_pages_list(self):
        """Get the Site Pages list"""
        result = self.client.sites.root.lists.get_by_name("Site Pages").get().execute_query()
        self.assertIsNotNone(result.resource_path)
