from enum import Enum


class WindowsDeviceType(Enum):
    none = "0"
    desktop = "1"
    mobile = "2"
    holographic = "4"
    team = "8"
    unknownFutureValue = "16"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsDeviceType"
