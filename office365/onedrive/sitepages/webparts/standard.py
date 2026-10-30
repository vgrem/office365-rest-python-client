from typing import Optional

from office365.onedrive.sitepages.webparts.data import WebPartData
from office365.onedrive.sitepages.webparts.web_part import WebPart
from office365.runtime.types.odata_property import odata


class StandardWebPart(WebPart):
    """Represents a standard web part instance on a SharePoint page."""

    @odata(name="containerTextWebPartId")
    @property
    def container_text_web_part_id(self) -> Optional[str]:
        """The instance identifier of the container text webPart. It only works for inline standard webPart in
        rich text webParts."""
        return self.properties.get("containerTextWebPartId", None)

    @odata(name="data")
    @property
    def data(self) -> Optional[WebPartData]:
        """Data of the webPart."""
        return self.properties.get("data", WebPartData())

    @odata(name="webPartType")
    @property
    def web_part_type(self) -> Optional[str]:
        """A Guid that indicates the webPart type."""
        return self.properties.get("webPartType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StandardWebPart"
