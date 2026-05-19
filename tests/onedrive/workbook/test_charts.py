import os
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.workbooks.charts.chart import WorkbookChart
from office365.onedrive.workbooks.worksheets.worksheet import WorkbookWorksheet
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestExcelCharts(GraphDelegatedTestCase):
    excel_file: Optional[DriveItem] = None
    worksheet: Optional[WorkbookWorksheet] = None
    chart: Optional[WorkbookChart] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        path = f"{os.path.dirname(__file__)}/../../../examples/data/templates/Weight loss tracker.xlsx"
        cls.excel_file = cls.client.me.drive.root.upload_file(path).execute_query()
        assert cls.excel_file.resource_path is not None
        cls.worksheet = cls.excel_file.workbook.worksheets["Weight loss tracker"].get().execute_query()
        assert cls.worksheet.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        assert cls.excel_file is not None
        cls.excel_file.delete_object().execute_query_retry()

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator"])
    def test1_list_charts(self):
        """List all charts in the worksheet"""
        assert TestExcelCharts.worksheet is not None
        result = TestExcelCharts.worksheet.charts.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator"])
    def test2_get_chart_by_name(self):
        """Get a chart by name"""
        assert TestExcelCharts.worksheet is not None
        result = TestExcelCharts.worksheet.charts["Weight Tracker"].get().execute_query()
        assert result.resource_path is not None
        TestExcelCharts.chart = result

    @requires_delegated("Files.ReadWrite", or_roles=["Global Administrator"])
    def test3_get_image(self):
        """Get the chart image"""
        assert TestExcelCharts.chart is not None
        result = TestExcelCharts.chart.image().execute_query()
        self.assertIsNotNone(result.value)
