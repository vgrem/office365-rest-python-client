from office365.entity import Entity
from office365.onedrive.workbooks.charts.axis import WorkbookChartAxis
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class WorkbookChartAxes(Entity):
    """Represents the chart axes."""

    @odata(name="categoryAxis")
    @property
    def category_axis(self) -> WorkbookChartAxis:
        """Represents the category axis in a chart."""
        return self.properties.get(
            "categoryAxis",
            WorkbookChartAxis(self.context, ResourcePath("categoryAxis", self.resource_path)),
        )

    @odata(name="seriesAxis")
    @property
    def series_axis(self) -> WorkbookChartAxis:
        """Represents the series axis of a 3-dimensional chart."""
        return self.properties.get(
            "seriesAxis",
            WorkbookChartAxis(self.context, ResourcePath("seriesAxis", self.resource_path)),
        )

    @odata(name="valueAxis")
    @property
    def value_axis(self) -> WorkbookChartAxis:
        """Represents the value axis in an axis."""
        return self.properties.get(
            "valueAxis",
            WorkbookChartAxis(self.context, ResourcePath("valueAxis", self.resource_path)),
        )
