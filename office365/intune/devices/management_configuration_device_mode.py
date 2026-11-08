from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationDeviceMode(Enum):
    none = "0"
    kiosk = "1"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationDeviceMode"
