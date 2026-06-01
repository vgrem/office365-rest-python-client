from typing import Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.sitepages.webparts.web_part import WebPart
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class HorizontalSectionColumn(Entity):
    """Represents a vertical column in a given horizontal section."""

    @odata(name="webParts")
    @property
    def web_parts(self) -> EntityCollection[WebPart]:
        """The set of web parts in this section."""
        return self.properties.get(
            "webParts", EntityCollection(self.context, WebPart, ResourcePath("webParts", self.resource_path))
        )

    @property
    def width(self) -> Optional[int]:
        """Gets the width property"""
        return self.properties.get("width", None)

    @property
    def webparts(self) -> EntityCollection[WebPart]:
        """Gets the webparts property"""
        return self.properties.get(
            "webparts", EntityCollection[WebPart](self.context, WebPart, ResourcePath("webparts", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.HorizontalSectionColumn"
