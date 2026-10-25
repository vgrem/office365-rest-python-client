from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class VideoThumbnail(Entity):
    @odata(name="Choice")
    @property
    def choice(self) -> Optional[int]:
        """Gets the Choice property"""
        return self.properties.get("Choice", None)

    @odata(name="IsSelected")
    @property
    def is_selected(self) -> Optional[bool]:
        """Gets the IsSelected property"""
        return self.properties.get("IsSelected", None)

    @odata(name="Url")
    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoThumbnail"
