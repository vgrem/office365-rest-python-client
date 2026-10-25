from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SmartCacheItem(Entity):
    """ """

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.SmartCache.SmartCacheItem"

    @odata(name="accessUrl")
    @property
    def access_url(self) -> Optional[str]:
        """Gets the accessUrl property"""
        return self.properties.get("accessUrl", None)

    @odata(name="containerTitle")
    @property
    def container_title(self) -> Optional[str]:
        """Gets the containerTitle property"""
        return self.properties.get("containerTitle", None)

    @odata(name="contentClass")
    @property
    def content_class(self) -> Optional[str]:
        """Gets the contentClass property"""
        return self.properties.get("contentClass", None)

    @odata(name="isDefaultDocumentLibrary")
    @property
    def is_default_document_library(self) -> Optional[bool]:
        """Gets the isDefaultDocumentLibrary property"""
        return self.properties.get("isDefaultDocumentLibrary", None)

    @odata(name="isTeamsChannelSite")
    @property
    def is_teams_channel_site(self) -> Optional[bool]:
        """Gets the isTeamsChannelSite property"""
        return self.properties.get("isTeamsChannelSite", None)

    @odata(name="isTeamsConnectedSite")
    @property
    def is_teams_connected_site(self) -> Optional[bool]:
        """Gets the isTeamsConnectedSite property"""
        return self.properties.get("isTeamsConnectedSite", None)

    @odata(name="lastAccessDateTime")
    @property
    def last_access_datetime(self) -> Optional[datetime]:
        """Gets the lastAccessDateTime property"""
        return self.properties.get("lastAccessDateTime", datetime.min)

    @odata(name="listId")
    @property
    def list_id(self) -> Optional[UUID]:
        """Gets the listId property"""
        return self.properties.get("listId", None)

    @odata(name="listItemId")
    @property
    def list_item_id(self) -> Optional[int]:
        """Gets the listItemId property"""
        return self.properties.get("listItemId", None)

    @odata(name="operation")
    @property
    def operation(self) -> Optional[int]:
        """Gets the operation property"""
        return self.properties.get("operation", None)

    @odata(name="pinOrder")
    @property
    def pin_order(self) -> Optional[int]:
        """Gets the pinOrder property"""
        return self.properties.get("pinOrder", None)

    @odata(name="siteAcronym")
    @property
    def site_acronym(self) -> Optional[str]:
        """Gets the siteAcronym property"""
        return self.properties.get("siteAcronym", None)

    @odata(name="siteColor")
    @property
    def site_color(self) -> Optional[str]:
        """Gets the siteColor property"""
        return self.properties.get("siteColor", None)

    @odata(name="siteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the siteId property"""
        return self.properties.get("siteId", None)

    @odata(name="siteLogoUrl")
    @property
    def site_logo_url(self) -> Optional[str]:
        """Gets the siteLogoUrl property"""
        return self.properties.get("siteLogoUrl", None)

    @odata(name="spoId")
    @property
    def spo_id(self) -> Optional[str]:
        """Gets the spoId property"""
        return self.properties.get("spoId", None)

    @odata(name="title")
    @property
    def title(self) -> Optional[str]:
        """Gets the title property"""
        return self.properties.get("title", None)

    @odata(name="uniqueId")
    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the uniqueId property"""
        return self.properties.get("uniqueId", None)

    @odata(name="webId")
    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the webId property"""
        return self.properties.get("webId", None)

    @odata(name="webUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the webUrl property"""
        return self.properties.get("webUrl", None)
