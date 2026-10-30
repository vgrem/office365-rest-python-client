from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.onedrive.workbooks.ranges.format import WorkbookRangeFormat
from office365.onedrive.workbooks.ranges.sort import WorkbookRangeSort
from office365.onedrive.workbooks.ranges.view import WorkbookRangeView
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.json import Json
from office365.runtime.types.odata_property import odata


class WorkbookRange(Entity):
    """Range represents a set of one or more contiguous cells such as a cell, a row, a column, block of cells, etc."""

    def __repr__(self):
        return self.address or self.entity_type_name

    def __str__(self):
        return self.address or self.entity_type_name

    def cell(self, row, column):
        """Gets the range object containing the single cell based on row and column numbers. The cell can be outside
        the bounds of its parent range, so long as it's stays within the worksheet grid.

        Args:
            row (int): Row number of the cell to be retrieved. Zero-indexed.
            column (int): Column number of the cell to be retrieved. Zero-indexed.
        """
        return_type = WorkbookRange(self.context)
        params = {"row": row, "column": column}
        qry = FunctionQuery(self, "cell", params, return_type=return_type)
        self.context.add_query(qry)
        return return_type

    def clear(self, apply_to=None):
        """Clear range values such as format, fill, and border.

        Args:
            apply_to (str):
        """
        payload = {"applyTo": apply_to}
        qry = ServiceOperationQuery(self, "clear", parameters_type=payload)
        self.context.add_query(qry)
        return self

    def insert(self, shift):
        """Inserts a cell or a range of cells into the worksheet in place of this range, and shifts the other cells to
        make space. Returns a new Range object at the now blank space.

        Args:
            shift (str): Specifies which way to shift the cells. The possible values are: Down, Right.
        """
        return_type = WorkbookRange(self.context)
        payload = {"shift": shift}
        qry = ServiceOperationQuery(self, "insert", parameters_type=payload, return_type=return_type)
        self.context.add_query(qry)
        return return_type

    def last_row(self):
        """
        Get the last row within the range. For example, the last row of B2:D5 is B5:D5.
        """
        return_type = WorkbookRange(self.context)
        qry = FunctionQuery(self, "lastRow", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    def visible_view(self):
        """Get the range visible from a filtered range."""
        return_type = WorkbookRangeView(self.context)
        qry = FunctionQuery(self, "visibleView", return_type=return_type)
        self.context.add_query(qry)
        return return_type

    def used_range(self, values_only=False):
        """Return the used range of the given range object.

        Args:
            values_only (bool): Optional. Considers only cells with values as used cells.
        """
        return_type = WorkbookRange(self.context)
        params = {"valuesOnly": values_only}
        qry = FunctionQuery(self, "usedRange", params, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="address")
    @property
    def address(self) -> Optional[str]:
        """
        Represents the range reference in A1-style. Address value will contain the Sheet reference
        (e.g. Sheet1!A1:B4)
        """
        return self.properties.get("address", None)

    @odata(name="addressLocal")
    @property
    def address_local(self) -> Optional[str]:
        """Represents range reference for the specified range in the language of the user."""
        return self.properties.get("addressLocal", None)

    @odata(name="cellCount")
    @property
    def cell_count(self) -> Optional[int]:
        """Number of cells in the range. Read-only."""
        return self.properties.get("cellCount", None)

    @odata(name="columnCount")
    @property
    def column_count(self) -> Optional[int]:
        """Represents the total number of columns in the range. Read-only."""
        return self.properties.get("columnCount", None)

    @odata(name="columnHidden")
    @property
    def column_hidden(self) -> Optional[bool]:
        """Represents if all columns of the current range are hidden."""
        return self.properties.get("columnHidden", None)

    @odata(name="columnIndex")
    @property
    def column_index(self) -> Optional[int]:
        """Represents the column number of the first cell in the range. Zero-indexed. Read-only."""
        return self.properties.get("columnIndex", None)

    @odata(name="rowIndex")
    @property
    def row_index(self) -> Optional[int]:
        """Returns the row number of the first cell in the range. Zero-indexed. Read-only."""
        return self.properties.get("rowIndex", None)

    @odata(name="format", navigation=True)
    @property
    def format(self):
        """Returns a format object, encapsulating the range's font, fill, borders, alignment, and other properties"""
        return self.properties.get(
            "format",
            WorkbookRangeFormat(self.context, ResourcePath("format", self.resource_path)),
        )

    @odata(name="sort", navigation=True)
    @property
    def sort(self):
        """The worksheet containing the current range."""
        return self.properties.get(
            "sort",
            WorkbookRangeSort(self.context, ResourcePath("sort", self.resource_path)),
        )

    @odata(name="values")
    @property
    def values(self) -> list | None:
        """Represents the raw values of the specified range. The data returned could be of type string, number,
        or a boolean. Cell that contains an error returns the error string."""
        return self.properties.get("values", None)

    @odata(name="valueTypes")
    @property
    def value_types(self) -> list | None:
        """Represents the type of data of each cell. The possible values are:
        Unknown, Empty, String, Integer, Double, Boolean, Error."""
        return self.properties.get("valueTypes", None)

    @odata(name="worksheet", navigation=True)
    @property
    def worksheet(self):
        """The worksheet containing the current range"""
        from office365.onedrive.workbooks.worksheets.worksheet import WorkbookWorksheet

        return self.properties.get(
            "worksheet",
            WorkbookWorksheet(self.context, ResourcePath("worksheet", self.resource_path)),
        )

    @odata(name="formulas")
    @property
    def formulas(self) -> Json:
        """Gets the formulas property"""
        return self.properties.get("formulas", Json())

    @odata(name="formulasLocal")
    @property
    def formulas_local(self) -> Json:
        """Gets the formulasLocal property"""
        return self.properties.get("formulasLocal", Json())

    @odata(name="formulasR1C1")
    @property
    def formulas_r1_c1(self) -> Json:
        """Gets the formulasR1C1 property"""
        return self.properties.get("formulasR1C1", Json())

    @odata(name="hidden")
    @property
    def hidden(self) -> Optional[bool]:
        """Gets the hidden property"""
        return self.properties.get("hidden", None)

    @odata(name="numberFormat")
    @property
    def number_format(self) -> Json:
        """Gets the numberFormat property"""
        return self.properties.get("numberFormat", Json())

    @odata(name="rowCount")
    @property
    def row_count(self) -> Optional[int]:
        """Gets the rowCount property"""
        return self.properties.get("rowCount", None)

    @odata(name="rowHidden")
    @property
    def row_hidden(self) -> Optional[bool]:
        """Gets the rowHidden property"""
        return self.properties.get("rowHidden", None)

    @odata(name="text")
    @property
    def text(self) -> Json:
        """Gets the text property"""
        return self.properties.get("text", Json())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookRange"
