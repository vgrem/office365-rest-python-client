from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.onedrive.workbooks.charts.legend.format import (
        WorkbookChartLegendFormat,
    )


class WorkbookChartLegend(Entity):
    """Represents the legend in a chart."""

    @odata(name="overlay")
    @property
    def overlay(self) -> Optional[bool]:
        """Indicates whether the chart legend should overlap with the main body of the chart."""
        return self.properties.get("overlay", None)

    @odata(name="position")
    @property
    def position(self) -> Optional[str]:
        """Represents the position of the legend on the chart.
        The possible values are: Top, Bottom, Left, Right, Corner, Custom."""
        return self.properties.get("position", None)

    @odata(name="visible")
    @property
    def visible(self) -> Optional[bool]:
        """Indicates whether the chart legend is visible."""
        return self.properties.get("visible", None)

    @odata(name="format", navigation=True)
    @property
    def format(self) -> WorkbookChartLegendFormat:
        """Gets the format property"""
        from office365.onedrive.workbooks.charts.legend.format import (
            WorkbookChartLegendFormat,
        )

        return self.properties.get(
            "format", WorkbookChartLegendFormat(self.context, ResourcePath("format", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookChartLegend"
