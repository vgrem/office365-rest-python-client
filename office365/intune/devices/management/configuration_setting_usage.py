from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationSettingUsage(Enum):
    none = "0"
    configuration = "1"
    compliance = "2"
    reusableSetting = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingUsage"
