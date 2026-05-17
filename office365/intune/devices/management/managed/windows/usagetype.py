from enum import Enum


class WindowsDeviceUsageType(Enum):
    singleUser = "0"
    shared = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsDeviceUsageType"
