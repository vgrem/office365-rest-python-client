from typing import List

from office365.onedrive.columns.definition import ColumnDefinition
from tests import create_unique_name
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestColumn(GraphTestCase):
    list_columns: List[ColumnDefinition] = []

    @classmethod
    def setUpClass(cls):
        super(TestColumn, cls).setUpClass()
        cls.doclib = cls.client.sites.root.lists["Documents"]

    @requires_delegated_permission(
        "Sites.Read.All",
        "Sites.Manage.All",
        "Sites.FullControl.All",
        "Sites.ReadWrite.All",
    )
    def test1_list_list_columns(self):
        columns = self.doclib.columns.get().execute_query()
        self.assertGreater(len(columns), 0)

    @requires_delegated_permission("Sites.Manage.All", "Sites.FullControl.All")
    def test2_create_text_column_for_list(self):
        column_name = create_unique_name("TextColumn")
        column = self.doclib.columns.add_text(column_name).execute_query()
        self.assertIsNotNone(column.resource_path)
        self.__class__.list_columns.append(column)

    @requires_delegated_permission("Sites.Manage.All", "Sites.FullControl.All")
    def test3_create_lookup_column_for_list(self):
        column_name = create_unique_name("LookupColumn")
        column = self.doclib.columns.add_lookup(column_name, self.doclib).execute_query()
        self.assertIsNotNone(column.resource_path)
        self.__class__.list_columns.append(column)

    @requires_delegated_permission("Sites.Manage.All", "Sites.FullControl.All")
    def test3_delete_list_columns(self):
        for col_to_del in self.__class__.list_columns:
            col_to_del.delete_object().execute_query()
