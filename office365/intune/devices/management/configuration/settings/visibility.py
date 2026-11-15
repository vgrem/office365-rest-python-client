from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationSettingVisibility(Enum):
    none = "0"
    settingsCatalog = "1"
    template = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingVisibility"
