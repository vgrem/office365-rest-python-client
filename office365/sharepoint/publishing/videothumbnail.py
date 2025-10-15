from typing import Optional

from office365.sharepoint.entity import Entity


class VideoThumbnail(Entity):

    @property
    def choice(self) -> Optional[int]:
        """Gets the Choice property"""
        return self.properties.get("Choice", None)

    @property
    def is_selected(self) -> Optional[bool]:
        """Gets the IsSelected property"""
        return self.properties.get("IsSelected", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoThumbnail"
