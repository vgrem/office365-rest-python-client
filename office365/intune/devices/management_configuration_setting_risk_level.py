from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationSettingRiskLevel(Enum):
    low = "0"
    medium = "1"
    high = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingRiskLevel"
