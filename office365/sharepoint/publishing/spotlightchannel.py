from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class SpotlightChannel(Entity):
    @property
    def channel_id(self) -> Optional[UUID]:
        """Gets the ChannelId property"""
        return self.properties.get("ChannelId", None)

    @property
    def tile_html_color(self) -> Optional[str]:
        """Gets the TileHtmlColor property"""
        return self.properties.get("TileHtmlColor", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def video_library_server_relative_url(self) -> Optional[str]:
        """Gets the VideoLibraryServerRelativeUrl property"""
        return self.properties.get("VideoLibraryServerRelativeUrl", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.SpotlightChannel"
