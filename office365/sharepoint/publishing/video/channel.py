from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.publishing.search import Search
from office365.sharepoint.publishing.spotlightvideo import SpotlightVideo
from office365.sharepoint.publishing.video.item import VideoItem


class VideoChannel(Entity):
    def get_video_count(self):
        return_type = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "GetVideoCount", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Publishing.VideoChannel"

    @odata(name="CanAdministrateByCurrent")
    @property
    def can_administrate_by_current(self) -> Optional[bool]:
        """Gets the CanAdministrateByCurrent property"""
        return self.properties.get("CanAdministrateByCurrent", None)

    @odata(name="CanEditByCurrent")
    @property
    def can_edit_by_current(self) -> Optional[bool]:
        """Gets the CanEditByCurrent property"""
        return self.properties.get("CanEditByCurrent", None)

    @odata(name="CanViewByCurrent")
    @property
    def can_view_by_current(self) -> Optional[bool]:
        """Gets the CanViewByCurrent property"""
        return self.properties.get("CanViewByCurrent", None)

    @odata(name="ChannelPageUrl")
    @property
    def channel_page_url(self) -> Optional[str]:
        """Gets the ChannelPageUrl property"""
        return self.properties.get("ChannelPageUrl", None)

    @odata(name="Description")
    @property
    def description(self) -> Optional[str]:
        """Gets the Description property"""
        return self.properties.get("Description", None)

    @odata(name="DownloadUrlVisibleMinPermission")
    @property
    def download_url_visible_min_permission(self) -> Optional[int]:
        """Gets the DownloadUrlVisibleMinPermission property"""
        return self.properties.get("DownloadUrlVisibleMinPermission", None)

    @odata(name="FullUrl")
    @property
    def full_url(self) -> Optional[str]:
        """Gets the FullUrl property"""
        return self.properties.get("FullUrl", None)

    @odata(name="Id")
    @property
    def id_(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="ServerRelativeUrl")
    @property
    def server_relative_url(self) -> Optional[str]:
        """Gets the ServerRelativeUrl property"""
        return self.properties.get("ServerRelativeUrl", None)

    @odata(name="ShareByEmailEnabled")
    @property
    def share_by_email_enabled(self) -> Optional[bool]:
        """Gets the ShareByEmailEnabled property"""
        return self.properties.get("ShareByEmailEnabled", None)

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

    @odata(name="YammerDefaultGroupId")
    @property
    def yammer_default_group_id(self) -> Optional[int]:
        """Gets the YammerDefaultGroupId property"""
        return self.properties.get("YammerDefaultGroupId", None)

    @odata(name="YammerEnabled")
    @property
    def yammer_enabled(self) -> Optional[bool]:
        """Gets the YammerEnabled property"""
        return self.properties.get("YammerEnabled", None)

    @odata(name="Search", navigation=True)
    @property
    def search(self) -> Search:
        """Gets the Search property"""
        return self.properties.get("Search", Search(self.context, ResourcePath("Search", self.resource_path)))

    @odata(name="SpotlightVideos", navigation=True)
    @property
    def spotlight_videos(self) -> EntityCollection[SpotlightVideo]:
        """Gets the SpotlightVideos property"""
        return self.properties.get(
            "SpotlightVideos",
            EntityCollection[SpotlightVideo](
                self.context, SpotlightVideo, ResourcePath("SpotlightVideos", self.resource_path)
            ),
        )

    @odata(name="Videos", navigation=True)
    @property
    def videos(self) -> EntityCollection[VideoItem]:
        """Gets the Videos property"""
        return self.properties.get(
            "Videos", EntityCollection[VideoItem](self.context, VideoItem, ResourcePath("Videos", self.resource_path))
        )

    def get_channel_page_url(self, view_mode: int) -> ClientResult[str]:
        """GetChannelPageUrl operation.

        Args:
            view_mode (int): viewMode parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "GetChannelPageUrl", [view_mode], return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
