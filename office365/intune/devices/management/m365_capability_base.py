from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.m365_capability_inbound_access import M365CapabilityInboundAccess
from office365.runtime.types.odata_property import key, odata


@key("name")
class M365CapabilityBase(Entity):
    @odata(name="inboundAccess")
    @property
    def inbound_access(self) -> Optional[M365CapabilityInboundAccess]:
        """Gets the inboundAccess property"""
        return self.properties.get("inboundAccess", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.M365CapabilityBase"
