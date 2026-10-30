from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onedrive.workbooks.charts.gridlines_format import (
        WorkbookChartGridlinesFormat,
    )


class WorkbookChartGridlines(Entity):
    @odata(name="visible")
    @property
    def visible(self) -> Optional[bool]:
        """Gets the visible property"""
        return self.properties.get("visible", None)

    @odata(name="format", navigation=True)
    @property
    def format(self) -> WorkbookChartGridlinesFormat:
        """Gets the format property"""
        from office365.onedrive.workbooks.charts.gridlines_format import (
            WorkbookChartGridlinesFormat,
        )

        return self.properties.get(
            "format", WorkbookChartGridlinesFormat(self.context, ResourcePath("format", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookChartGridlines"
