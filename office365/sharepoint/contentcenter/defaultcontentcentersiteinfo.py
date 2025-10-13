from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class DefaultContentCenterSiteInfo(Entity):

    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @property
    def site_name(self) -> Optional[str]:
        """Gets the SiteName property"""
        return self.properties.get("SiteName", None)

    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def web_id(self) -> Optional[UUID]:
        """Gets the WebId property"""
        return self.properties.get("WebId", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.DefaultContentCenterSiteInfo"
