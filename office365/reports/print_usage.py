from __future__ import annotations

from datetime import date
from typing import Optional

from office365.entity import Entity


class PrintUsage(Entity):
    @property
    def black_and_white_page_count(self) -> Optional[int]:
        """Gets the blackAndWhitePageCount property"""
        return self.properties.get("blackAndWhitePageCount", None)

    @property
    def color_page_count(self) -> Optional[int]:
        """Gets the colorPageCount property"""
        return self.properties.get("colorPageCount", None)

    @property
    def completed_black_and_white_job_count(self) -> Optional[int]:
        """Gets the completedBlackAndWhiteJobCount property"""
        return self.properties.get("completedBlackAndWhiteJobCount", None)

    @property
    def completed_color_job_count(self) -> Optional[int]:
        """Gets the completedColorJobCount property"""
        return self.properties.get("completedColorJobCount", None)

    @property
    def completed_job_count(self) -> Optional[int]:
        """Gets the completedJobCount property"""
        return self.properties.get("completedJobCount", None)

    @property
    def double_sided_sheet_count(self) -> Optional[int]:
        """Gets the doubleSidedSheetCount property"""
        return self.properties.get("doubleSidedSheetCount", None)

    @property
    def incomplete_job_count(self) -> Optional[int]:
        """Gets the incompleteJobCount property"""
        return self.properties.get("incompleteJobCount", None)

    @property
    def media_sheet_count(self) -> Optional[int]:
        """Gets the mediaSheetCount property"""
        return self.properties.get("mediaSheetCount", None)

    @property
    def page_count(self) -> Optional[int]:
        """Gets the pageCount property"""
        return self.properties.get("pageCount", None)

    @property
    def single_sided_sheet_count(self) -> Optional[int]:
        """Gets the singleSidedSheetCount property"""
        return self.properties.get("singleSidedSheetCount", None)

    @property
    def usage_date(self) -> Optional[date]:
        """Gets the usageDate property"""
        return self.properties.get("usageDate", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrintUsage"
