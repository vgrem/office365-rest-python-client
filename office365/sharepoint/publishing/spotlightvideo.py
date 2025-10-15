from typing import Optional

from office365.sharepoint.entity import Entity


class SpotlightVideo(Entity):

    @property
    def server_relative_url(self) -> Optional[str]:
        """Gets the ServerRelativeUrl property"""
        return self.properties.get("ServerRelativeUrl", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.SpotlightVideo"
