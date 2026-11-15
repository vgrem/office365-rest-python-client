from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.health_state import HealthState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsManagementAppHealthState(Entity):
    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="deviceOSVersion")
    @property
    def device_os_version(self) -> Optional[str]:
        """Gets the deviceOSVersion property"""
        return self.properties.get("deviceOSVersion", None)

    @odata(name="installedVersion")
    @property
    def installed_version(self) -> Optional[str]:
        """Gets the installedVersion property"""
        return self.properties.get("installedVersion", None)

    @odata(name="lastCheckInDateTime")
    @property
    def last_check_in_date_time(self) -> Optional[datetime]:
        """Gets the lastCheckInDateTime property"""
        return self.properties.get("lastCheckInDateTime", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagementAppHealthState"

    @odata(name="healthState")
    @property
    def health_state(self) -> Optional[HealthState]:
        """Gets the healthState property"""
        return self.properties.get("healthState", None)
