from typing import List

from office365.onedrive.columns.definition import ColumnDefinition
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestColumn(GraphDelegatedTestCase):
    list_columns: List[ColumnDefinition] = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doclib = cls.client.sites.root.lists["Documents"]

    @requires_delegated(
        "Sites.Read.All",
        "Sites.Manage.All",
        "Sites.FullControl.All",
        "Sites.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test1_list_list_columns(self):
        """List all columns in the document library"""
        columns = self.doclib.columns.get().execute_query()
        self.assertGreater(len(columns), 0)

    @requires_delegated("Sites.Manage.All", "Sites.FullControl.All", or_roles=["Global Administrator"])
    def test2_create_text_column_for_list(self):
        """Create a text column for the document library"""
        column_name = create_unique_name("TextColumn")
        column = self.doclib.columns.add_text(column_name).execute_query()
        assert column.resource_path is not None
        TestColumn.list_columns.append(column)

    @requires_delegated("Sites.Manage.All", "Sites.FullControl.All", or_roles=["Global Administrator"])
    def test3_create_lookup_column_for_list(self):
        """Create a lookup column for the document library"""
        column_name = create_unique_name("LookupColumn")
        column = self.doclib.columns.add_lookup(column_name, self.doclib).execute_query()
        assert column.resource_path is not None
        TestColumn.list_columns.append(column)

    @requires_delegated("Sites.Manage.All", "Sites.FullControl.All", or_roles=["Global Administrator"])
    def test3_delete_list_columns(self):
        """Delete previously created list columns"""
        for col_to_del in TestColumn.list_columns:
            col_to_del.delete_object().execute_query()
