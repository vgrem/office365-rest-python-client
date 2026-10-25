from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TenantDataLossPreventionQuarantineSettings(Entity):
    @odata(name="QuarantineLocation")
    @property
    def quarantine_location(self) -> Optional[str]:
        """Gets the QuarantineLocation property"""
        return self.properties.get("QuarantineLocation", None)

    @odata(name="TombstoneText")
    @property
    def tombstone_text(self) -> Optional[str]:
        """Gets the TombstoneText property"""
        return self.properties.get("TombstoneText", None)
