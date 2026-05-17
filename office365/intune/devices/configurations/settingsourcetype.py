from enum import Enum


class SettingSourceType(Enum):
    deviceConfiguration = "0"
    deviceIntent = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SettingSourceType"
