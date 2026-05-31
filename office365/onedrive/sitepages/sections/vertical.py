from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.onedrive.sitepages.webparts.web_part import WebPart
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class VerticalSection(Entity):
    """Represents the vertical section in a given SharePoint page."""

    @odata(name="webParts")
    @property
    def web_parts(self) -> EntityCollection[WebPart]:
        """The set of web parts in this vertical section."""
        return self.properties.get(
            "webParts",
            EntityCollection(self.context, WebPart, ResourcePath("webParts", self.resource_path)),
        )
