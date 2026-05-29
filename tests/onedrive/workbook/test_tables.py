import os
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.workbooks.sort_field import WorkbookSortField
from office365.onedrive.workbooks.tables.table import WorkbookTable
from office365.onedrive.workbooks.worksheets.worksheet import WorkbookWorksheet
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestExcelTables(GraphDelegatedTestCase):
    excel_file: Optional[DriveItem] = None
    worksheet: Optional[WorkbookWorksheet] = None
    table: Optional[WorkbookTable] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        path = f"{os.path.dirname(__file__)}/../../data/Financial Sample.xlsx"
        cls.excel_file = cls.client.me.drive.root.upload_file(path).execute_query()
        assert cls.excel_file.resource_path is not None
        cls.worksheet = cls.excel_file.workbook.worksheets["Sheet1"].get().execute_query()
        assert cls.worksheet.resource_path is not None
        cls.table = cls.worksheet.tables["financials"].get().execute_query()
        assert cls.table.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        assert cls.excel_file is not None
        cls.excel_file.delete_object().execute_query_retry()

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test1_sort_apply(self):
        """Apply sorting to a table"""
        sort_fields = [WorkbookSortField()]
        assert TestExcelTables.table is not None
        result = TestExcelTables.table.sort.apply(sort_fields).execute_query()
        self.assertIsNotNone(result.resource_path)
