from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TeamResource(Entity):
    """ """

    @odata(name="DisplayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @odata(name="SiteLogoUrl")
    @property
    def site_logo_url(self) -> Optional[str]:
        """Gets the SiteLogoUrl property"""
        return self.properties.get("SiteLogoUrl", None)

    @odata(name="Visibility")
    @property
    def visibility(self) -> Optional[str]:
        """Gets the Visibility property"""
        return self.properties.get("Visibility", None)

    @odata(name="WebUrl")
    @property
    def web_url(self) -> Optional[str]:
        """Gets the WebUrl property"""
        return self.properties.get("WebUrl", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.Teams.TeamResource"

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)
