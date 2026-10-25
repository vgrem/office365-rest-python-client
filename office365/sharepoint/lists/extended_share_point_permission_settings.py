from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ExtendedSharePointPermissionSettings(Entity):
    @odata(name="Enabled")
    @property
    def enabled(self) -> Optional[bool]:
        """Gets the Enabled property"""
        return self.properties.get("Enabled", None)

    @odata(name="OfflineDays")
    @property
    def offline_days(self) -> Optional[int]:
        """Gets the OfflineDays property"""
        return self.properties.get("OfflineDays", None)
