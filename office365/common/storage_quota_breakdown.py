from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class StorageQuotaBreakdown(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="manageWebUrl")
    @property
    def manage_web_url(self) -> Optional[str]:
        """Gets the manageWebUrl property"""
        return self.properties.get("manageWebUrl", None)

    @odata(name="used")
    @property
    def used(self) -> Optional[int]:
        """Gets the used property"""
        return self.properties.get("used", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.StorageQuotaBreakdown"
