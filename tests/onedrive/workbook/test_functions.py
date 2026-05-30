import os
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.workbooks.tables.table import WorkbookTable
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestExcelFunctions(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    target_item: Optional[DriveItem] = None
    table: Optional[WorkbookTable] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        path = f"{os.path.dirname(__file__)}/../../data/Financial Sample.xlsx"
        cls.target_item = cls.client.me.drive.root.upload_file(path).execute_query()
        assert cls.target_item.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        assert cls.target_item is not None
        cls.target_item.delete_object().execute_query_retry()

    @requires_delegated("Files.ReadWrite", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test1_get_abs(self):
        """Test the ABS workbook function"""
        assert TestExcelFunctions.target_item is not None
        result = TestExcelFunctions.target_item.workbook.functions.abs(-2).execute_query()
        self.assertEqual(result.value, 2)

    # def test2_get_days(self):
    #    start = datetime.now()
    #    end = start + timedelta(days=10)
    #    result = self.__class__.target_item.workbook.functions.days(
    #        start, end
    #    ).execute_query()
    #    self.assertGreater(result.value, 1)
