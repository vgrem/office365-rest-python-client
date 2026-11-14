from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementDomainJoinConnector(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastConnectionDateTime")
    @property
    def last_connection_date_time(self) -> Optional[datetime]:
        """Gets the lastConnectionDateTime property"""
        return self.properties.get("lastConnectionDateTime", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementDomainJoinConnector"
