from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.managed.ebook.installstate import InstallState
from office365.runtime.types.odata_property import odata


class DeviceInstallState(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="errorCode")
    @property
    def error_code(self) -> Optional[str]:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", None)

    @odata(name="installState")
    @property
    def install_state(self) -> InstallState:
        """Gets the installState property"""
        return self.properties.get("installState", InstallState.notApplicable)

    @odata(name="lastSyncDateTime")
    @property
    def last_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastSyncDateTime property"""
        return self.properties.get("lastSyncDateTime", datetime.min)

    @odata(name="osDescription")
    @property
    def os_description(self) -> Optional[str]:
        """Gets the osDescription property"""
        return self.properties.get("osDescription", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @odata(name="userName")
    @property
    def user_name(self) -> Optional[str]:
        """Gets the userName property"""
        return self.properties.get("userName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceInstallState"
