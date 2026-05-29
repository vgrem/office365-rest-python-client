from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.workbooks.worksheets.protection_options import (
    WorkbookWorksheetProtectionOptions,
)
from office365.onedrive.workbooks.worksheets.worksheet import WorkbookWorksheet
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase
from tests.onedrive.test_excel import upload_excel


class TestExcelWorksheets(GraphDelegatedTestCase):
    excel_file: Optional[DriveItem] = None
    sheet_name = create_unique_name("Sheet")
    worksheet: Optional[WorkbookWorksheet] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.excel_file = upload_excel(cls.client.me.drive)
        assert cls.excel_file.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        assert cls.excel_file is not None
        cls.excel_file.delete_object().execute_query_retry()

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test1_add_worksheet(self):
        """Add a new worksheet to the workbook"""
        assert TestExcelWorksheets.excel_file is not None
        result = TestExcelWorksheets.excel_file.workbook.worksheets.add(self.sheet_name).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test2_list_worksheets(self):
        """List all worksheets in the workbook"""
        assert TestExcelWorksheets.excel_file is not None
        result = TestExcelWorksheets.excel_file.workbook.worksheets.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 1)
        TestExcelWorksheets.worksheet = result[0]

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test3_used_range(self):
        """Get the used range of a worksheet"""
        assert TestExcelWorksheets.worksheet is not None
        result = TestExcelWorksheets.worksheet.used_range().execute_query()
        self.assertIsNotNone(result.address)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test4_protect_worksheet(self):
        """Protect a worksheet"""
        ws = TestExcelWorksheets.worksheet
        assert ws is not None
        options = WorkbookWorksheetProtectionOptions(allow_delete_rows=False)
        ws.protection.protect(options).execute_query()
        result = ws.protection.get().execute_query()
        self.assertFalse(result.options.allowDeleteRows)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test5_delete_worksheet(self):
        """Delete a worksheet"""
        assert TestExcelWorksheets.excel_file is not None
        worksheet = TestExcelWorksheets.excel_file.workbook.worksheets[self.sheet_name]
        worksheet.delete_object().execute_query()
