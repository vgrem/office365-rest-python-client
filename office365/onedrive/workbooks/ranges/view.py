from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.json import Json
from office365.runtime.types.odata_property import odata


class WorkbookRangeView(Entity):
    """Represents a set of visible cells of the parent range."""

    @odata(name="cellAddresses")
    @property
    def cell_addresses(self) -> Optional[dict]:
        """The cell addresses."""
        return self.properties.get("cellAddresses", None)

    @odata(name="columnCount")
    @property
    def column_count(self) -> Optional[int]:
        """The number of visible columns."""
        return self.properties.get("columnCount", None)

    @odata(name="rows", navigation=True)
    @property
    def rows(self) -> EntityCollection[WorkbookRangeView]:
        """Represents a collection of range views associated with the range."""
        return self.properties.get(
            "rows",
            EntityCollection(
                self.context,
                WorkbookRangeView,
                ResourcePath("rows", self.resource_path),
            ),
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

    @odata(name="index")
    @property
    def index(self) -> Optional[int]:
        """Gets the index property"""
        return self.properties.get("index", None)

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

    @odata(name="text")
    @property
    def text(self) -> Json:
        """Gets the text property"""
        return self.properties.get("text", Json())

    @odata(name="values")
    @property
    def values(self) -> Json:
        """Gets the values property"""
        return self.properties.get("values", Json())

    @odata(name="valueTypes")
    @property
    def value_types(self) -> Json:
        """Gets the valueTypes property"""
        return self.properties.get("valueTypes", Json())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookRangeView"
