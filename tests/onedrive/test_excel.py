import os
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.workbooks.tables.table import WorkbookTable
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


def upload_excel(target_drive: Drive) -> DriveItem:
    path = f"{os.path.dirname(__file__)}/../data/Financial Sample.xlsx"
    return target_drive.root.upload_file(path).execute_query()


class TestExcel(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    target_item: Optional[DriveItem] = None
    table: Optional[WorkbookTable] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_item = upload_excel(cls.client.me.drive)
        assert cls.target_item.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        assert cls.target_item is not None
        cls.target_item.delete_object().execute_query_retry()

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test1_get_workbook(self):
        """Get the workbook from the uploaded Excel file"""
        assert TestExcel.target_item is not None
        workbook = TestExcel.target_item.workbook.get().execute_query_retry()
        self.assertIsNotNone(workbook.resource_path)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test2_create_workbook_table(self):
        """Create a workbook table"""
        assert TestExcel.target_item is not None
        table = TestExcel.target_item.workbook.tables.add("A10000:C10002", True).execute_query()
        assert table.resource_path is not None
        TestExcel.table = table

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test3_list_workbook_tables(self):
        """List all workbook tables"""
        assert TestExcel.target_item is not None
        tables = TestExcel.target_item.workbook.tables.get().execute_query_retry()
        self.assertIsNotNone(tables.resource_path)
        self.assertGreater(len(tables), 0)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test4_data_body_range(self):
        """Get data body range of a table"""
        assert TestExcel.table is not None
        result = TestExcel.table.data_body_range().execute_query()
        self.assertIsNotNone(result.address)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test5_create_table_column(self):
        """Create a column in a workbook table"""
        assert TestExcel.table is not None
        column = TestExcel.table.columns.add(3, "Column4").execute_query()
        self.assertIsNotNone(column.resource_path)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test6_create_table_column_count(self):
        """Count columns in a workbook table"""
        assert TestExcel.table is not None
        result = TestExcel.table.columns.count().execute_query()
        self.assertGreater(result.value, 0)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test7_list_table_columns(self):
        """List all columns in a workbook table"""
        assert TestExcel.table is not None
        columns = TestExcel.table.columns.get().execute_query()
        self.assertIsNotNone(columns.resource_path)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test8_list_table_rows(self):
        """List all rows in a workbook table"""
        assert TestExcel.table is not None
        rows = TestExcel.table.rows.get().execute_query()
        self.assertIsNotNone(rows.resource_path)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test9_create_table_rows(self):
        """Create rows in a workbook table"""
        assert TestExcel.table is not None
        row = TestExcel.table.rows.add([["Val11", "Val12", "Val13", "Val14"]]).execute_query()
        self.assertIsNotNone(row.resource_path)
        self.assertIsNotNone(row.index)
        self.assertIsNotNone(row.values)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test_10_table_rows_count(self):
        """Count rows in a workbook table"""
        assert TestExcel.table is not None
        result = TestExcel.table.rows.count().execute_query()
        self.assertIsNotNone(result.value)
        self.assertGreater(result.value, 0)

    # def test_11_table_rows_item_at(self):
    #    result = self.__class__.table.rows.item_at(0).execute_query()
    #    self.assertIsNotNone(result.resource_path)
    #    self.assertIsNotNone(result.values)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test_12_table_range(self):
        """Get the range of a workbook table"""
        assert TestExcel.table is not None
        result = TestExcel.table.range().execute_query()
        self.assertIsNotNone(result.address)

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test_13_delete_workbook_table(self):
        """Delete a workbook table"""
        assert TestExcel.table is not None
        TestExcel.table.delete_object().execute_query()

    # def test_14_workbook_create_session(self):
    #    result = self.__class__.target_item.workbook.create_session().execute_query()
    #    self.assertIsNotNone(result.value)

    # def test_15_workbook_close_session(self):
    #    self.__class__.target_item.workbook.close_session().execute_query()
