from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.workbooks.names.named_item import WorkbookNamedItem
from office365.onedrive.workbooks.ranges.range import WorkbookRange
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase
from tests.onedrive.test_excel import upload_excel


class TestExcelRanges(GraphDelegatedTestCase):
    excel_file: Optional[DriveItem] = None
    named_item: Optional[WorkbookNamedItem] = None
    range: Optional[WorkbookRange] = None
    sheet_name = create_unique_name("Sheet")

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
    def test1_name_create(self):
        """Create a named item in the workbook"""
        assert TestExcelRanges.excel_file is not None
        result = TestExcelRanges.excel_file.workbook.names.add(
            "test5", "=Sheet1!$F$15:$N$27", "Comment for the named item"
        ).execute_query()
        assert result.resource_path is not None
        TestExcelRanges.named_item = result

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test2_names_get(self):
        """Get a named item"""
        assert TestExcelRanges.named_item is not None
        result = TestExcelRanges.named_item.get().execute_query_retry(2)
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test3_list_range(self):
        """Get the range of a named item"""
        assert TestExcelRanges.named_item is not None
        result = TestExcelRanges.named_item.range().execute_query()
        assert result.address is not None
        TestExcelRanges.range = result

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test4_last_row(self):
        """Get the last row of a range"""
        assert TestExcelRanges.range is not None
        result = TestExcelRanges.range.last_row().execute_query()
        self.assertIsNotNone(result.address)

    # def test4_insert_range(self):
    #    result = self.__class__.range.insert("Right").execute_query()
    #    self.assertIsNotNone(result.address)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test6_used_range(self):
        """Get the used range of a range"""
        assert TestExcelRanges.range is not None
        result = TestExcelRanges.range.used_range().execute_query()
        self.assertIsNotNone(result.address)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test7_clear_range(self):
        """Clear a range"""
        assert TestExcelRanges.range is not None
        result = TestExcelRanges.range.clear().execute_query()
        self.assertIsNotNone(result.address)
