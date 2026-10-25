from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.publishing.video.channel import VideoChannel


class SpotlightChannel(Entity):
    @odata(name="ChannelId")
    @property
    def channel_id(self) -> Optional[UUID]:
        """Gets the ChannelId property"""
        return self.properties.get("ChannelId", None)

    @odata(name="TileHtmlColor")
    @property
    def tile_html_color(self) -> Optional[str]:
        """Gets the TileHtmlColor property"""
        return self.properties.get("TileHtmlColor", None)

    @odata(name="Title")
    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @odata(name="VideoLibraryServerRelativeUrl")
    @property
    def video_library_server_relative_url(self) -> Optional[str]:
        """Gets the VideoLibraryServerRelativeUrl property"""
        return self.properties.get("VideoLibraryServerRelativeUrl", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.SpotlightChannel"

    @odata(name="Id")
    @property
    def id(self) -> Optional[int]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="Channel", navigation=True)
    @property
    def channel(self) -> VideoChannel:
        """Gets the Channel property"""
        from office365.sharepoint.publishing.video.channel import VideoChannel

        return self.properties.get("Channel", VideoChannel(self.context, ResourcePath("Channel", self.resource_path)))
