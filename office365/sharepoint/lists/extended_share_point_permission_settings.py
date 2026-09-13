from __future__ import annotations

from typing import Optional

from office365.sharepoint.entity import Entity


class ExtendedSharePointPermissionSettings(Entity):
    @property
    def enabled(self) -> Optional[bool]:
        """Gets the Enabled property"""
        return self.properties.get("Enabled", None)

    @property
    def offline_days(self) -> Optional[int]:
        """Gets the OfflineDays property"""
        return self.properties.get("OfflineDays", None)
