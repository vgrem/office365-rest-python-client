from enum import Enum


class WindowsSettingType(Enum):
    roaming = "0"
    backup = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsSettingType"
