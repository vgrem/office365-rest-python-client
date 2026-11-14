from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsManagementAppHealthSummary(Entity):
    @odata(name="healthyDeviceCount")
    @property
    def healthy_device_count(self) -> Optional[int]:
        """Gets the healthyDeviceCount property"""
        return self.properties.get("healthyDeviceCount", None)

    @odata(name="unhealthyDeviceCount")
    @property
    def unhealthy_device_count(self) -> Optional[int]:
        """Gets the unhealthyDeviceCount property"""
        return self.properties.get("unhealthyDeviceCount", None)

    @odata(name="unknownDeviceCount")
    @property
    def unknown_device_count(self) -> Optional[int]:
        """Gets the unknownDeviceCount property"""
        return self.properties.get("unknownDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsManagementAppHealthSummary"
