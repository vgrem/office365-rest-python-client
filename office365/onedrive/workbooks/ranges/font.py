from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class WorkbookRangeFont(Entity):
    """This object represents the font attributes (font name, font size, color, etc.) for an object."""

    @odata(name="bold")
    @property
    def bold(self) -> Optional[bool]:
        """Inidicates whether the font is bold."""
        return self.properties.get("bold", None)

    @odata(name="color")
    @property
    def color(self) -> Optional[str]:
        """The HTML color code representation of the text color. For example, #FF0000 represents the color red."""
        return self.properties.get("color", None)

    @odata(name="italic")
    @property
    def italic(self) -> Optional[bool]:
        """Inidicates whether the font is italic."""
        return self.properties.get("italic", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """The font name. For example, "Calibri"."""
        return self.properties.get("name", None)

    @odata(name="size")
    @property
    def size(self) -> Optional[float]:
        """The font size."""
        return self.properties.get("size", None)

    @odata(name="underline")
    @property
    def underline(self) -> Optional[bool]:
        """The type of underlining applied to the font. The possible values are:
        None, Single, Double, SingleAccountant, DoubleAccountant."""
        return self.properties.get("underline", None)
