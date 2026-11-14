from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementScriptRunSummary(Entity):
    @odata(name="errorDeviceCount")
    @property
    def error_device_count(self) -> Optional[int]:
        """Gets the errorDeviceCount property"""
        return self.properties.get("errorDeviceCount", None)

    @odata(name="errorUserCount")
    @property
    def error_user_count(self) -> Optional[int]:
        """Gets the errorUserCount property"""
        return self.properties.get("errorUserCount", None)

    @odata(name="successDeviceCount")
    @property
    def success_device_count(self) -> Optional[int]:
        """Gets the successDeviceCount property"""
        return self.properties.get("successDeviceCount", None)

    @odata(name="successUserCount")
    @property
    def success_user_count(self) -> Optional[int]:
        """Gets the successUserCount property"""
        return self.properties.get("successUserCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementScriptRunSummary"
