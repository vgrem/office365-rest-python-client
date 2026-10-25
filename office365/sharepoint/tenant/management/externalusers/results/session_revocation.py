from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPOUserSessionRevocationResult(Entity):
    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantManagement.SPOUserSessionRevocationResult"

    @odata(name="State")
    @property
    def state(self) -> Optional[int]:
        """Gets the State property"""
        return self.properties.get("State", None)
