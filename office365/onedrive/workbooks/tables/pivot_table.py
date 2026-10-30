from typing import Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


class WorkbookPivotTable(Entity):
    """Represents an Excel PivotTable."""

    def __str__(self):
        return self.name or self.entity_type_name

    def refresh(self) -> Self:
        """Refreshes the PivotTable."""
        qry = ServiceOperationQuery(self, "refresh")
        self.context.add_query(qry)
        return self

    def refresh_all(self) -> Self:
        """Refreshes the PivotTable within a given worksheet."""
        qry = ServiceOperationQuery(self, "refreshAll")
        self.context.add_query(qry)
        return self

    @property
    def name(self) -> Optional[str]:
        """Name of the PivotTable."""
        return self.properties.get("Name", None)

    @odata(name="worksheet", navigation=True)
    @property
    def worksheet(self):
        """The worksheet containing the current PivotTable"""
        from office365.onedrive.workbooks.worksheets.worksheet import WorkbookWorksheet

        return self.properties.get(
            "worksheet",
            WorkbookWorksheet(self.context, ResourcePath("worksheet", self.resource_path)),
        )
