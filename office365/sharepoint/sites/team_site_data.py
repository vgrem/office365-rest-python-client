from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TeamSiteData(Entity):
    """"""

    @odata(name="ErrorTag", beta=True)
    @property
    def error_tag(self) -> Optional[int]:
        """Gets the ErrorTag property"""
        return self.properties.get("ErrorTag", None)

    @odata(name="HeaderColorIndexInDarkMode", beta=True)
    @property
    def header_color_index_in_dark_mode(self) -> Optional[int]:
        """Gets the HeaderColorIndexInDarkMode property"""
        return self.properties.get("HeaderColorIndexInDarkMode", None)

    @odata(name="HeaderColorIndexInLightMode", beta=True)
    @property
    def header_color_index_in_light_mode(self) -> Optional[int]:
        """Gets the HeaderColorIndexInLightMode property"""
        return self.properties.get("HeaderColorIndexInLightMode", None)

    @odata(name="HeaderEmphasis", beta=True)
    @property
    def header_emphasis(self) -> Optional[int]:
        """Gets the HeaderEmphasis property"""
        return self.properties.get("HeaderEmphasis", None)

    @odata(name="HubSiteId", beta=True)
    @property
    def hub_site_id(self) -> Optional[UUID]:
        """Gets the HubSiteId property"""
        return self.properties.get("HubSiteId", None)

    @odata(name="SiteUrl", beta=True)
    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @odata(name="TenantInstanceId", beta=True)
    @property
    def tenant_instance_id(self) -> Optional[UUID]:
        """Gets the TenantInstanceId property"""
        return self.properties.get("TenantInstanceId", None)

    @odata(name="ThemeToken", beta=True)
    @property
    def theme_token(self) -> Optional[str]:
        """Gets the ThemeToken property"""
        return self.properties.get("ThemeToken", None)
