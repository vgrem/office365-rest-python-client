from __future__ import annotations

from enum import Enum


class DeviceManagementConfigurationSettingAccessTypes(Enum):
    none = "0"
    add = "1"
    copy = "2"
    delete = "4"
    get = "8"
    replace = "16"
    execute = "32"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingAccessTypes"
