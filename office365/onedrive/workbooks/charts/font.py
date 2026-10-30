from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WorkbookChartFont(Entity):
    """This object represents the font attributes (font name, font size, color, etc.) for a chart object."""

    @odata(name="bold")
    @property
    def bold(self) -> Optional[bool]:
        """Gets the bold property"""
        return self.properties.get("bold", None)

    @odata(name="color")
    @property
    def color(self) -> Optional[str]:
        """Gets the color property"""
        return self.properties.get("color", None)

    @odata(name="italic")
    @property
    def italic(self) -> Optional[bool]:
        """Gets the italic property"""
        return self.properties.get("italic", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="size")
    @property
    def size(self) -> Optional[float]:
        """Gets the size property"""
        return self.properties.get("size", None)

    @odata(name="underline")
    @property
    def underline(self) -> Optional[str]:
        """Gets the underline property"""
        return self.properties.get("underline", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkbookChartFont"
