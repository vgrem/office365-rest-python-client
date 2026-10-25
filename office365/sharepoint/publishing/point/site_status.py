from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class PointPublishingSiteStatus(Entity):
    @property
    def entity_type_name(self):
        return "SP.Publishing.PointPublishingSiteStatus"

    @odata(name="FriendlyUrl")
    @property
    def friendly_url(self) -> Optional[str]:
        """Gets the FriendlyUrl property"""
        return self.properties.get("FriendlyUrl", None)

    @odata(name="SiteId")
    @property
    def site_id(self) -> Optional[UUID]:
        """Gets the SiteId property"""
        return self.properties.get("SiteId", None)

    @odata(name="SiteUrl")
    @property
    def site_url(self) -> Optional[str]:
        """Gets the SiteUrl property"""
        return self.properties.get("SiteUrl", None)

    @odata(name="Status")
    @property
    def status(self) -> Optional[int]:
        """Gets the Status property"""
        return self.properties.get("Status", None)
