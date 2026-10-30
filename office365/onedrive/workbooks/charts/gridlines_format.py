from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onedrive.workbooks.charts.line_format import WorkbookChartLineFormat


class WorkbookChartGridlinesFormat(Entity):
    @odata(name="line", navigation=True)
    @property
    def line(self) -> WorkbookChartLineFormat:
        """Gets the line property"""
        from office365.onedrive.workbooks.charts.line_format import WorkbookChartLineFormat

        return self.properties.get(
            "line", WorkbookChartLineFormat(self.context, ResourcePath("line", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookChartGridlinesFormat"
