from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.onedrive.workbooks.filter import WorkbookFilter
from office365.onedrive.workbooks.ranges.range import WorkbookRange
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.json import Json
from office365.runtime.types.odata_property import odata


class WorkbookTableColumn(Entity):
    """Represents a column in a table."""

    def header_row_range(self) -> WorkbookRange:
        """
        Gets the range object associated with the header row of the column.
        """
        return_type = WorkbookRange(self.context)
        qry = FunctionQuery(self, "headerRowRange", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    def range(self) -> WorkbookRange:
        """
        Gets the range object associated with the entire column.
        """
        return_type = WorkbookRange(self.context)
        qry = FunctionQuery(self, "range", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="values")
    @property
    def values(self) -> Optional[Json]:
        """
        Represents the raw values of the specified range. The data returned could be of type string, number,
        or a boolean. Cell that contain an error will return the error string.
        """
        return self.properties.get("values", None)

    @odata(name="filter", navigation=True)
    @property
    def filter(self) -> WorkbookFilter:
        """Retrieve the filter applied to the column."""
        return self.properties.get(
            "filter",
            WorkbookFilter(self.context, ResourcePath("filter", self.resource_path)),
        )

    @odata(name="index")
    @property
    def index(self) -> Optional[int]:
        """Gets the index property"""
        return self.properties.get("index", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookTableColumn"
