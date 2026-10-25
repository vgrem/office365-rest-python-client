from __future__ import annotations

from typing import Optional
from uuid import UUID

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SPAuthEvent(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AuthPolicy.Events.SPAuthEvent"

    @odata(name="EventData")
    @property
    def event_data(self) -> Optional[str]:
        """Gets the EventData property"""
        return self.properties.get("EventData", None)

    @odata(name="EventSource")
    @property
    def event_source(self) -> Optional[int]:
        """Gets the EventSource property"""
        return self.properties.get("EventSource", None)

    @odata(name="TenantId")
    @property
    def tenant_id(self) -> Optional[UUID]:
        """Gets the TenantId property"""
        return self.properties.get("TenantId", None)
