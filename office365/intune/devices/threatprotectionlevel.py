from enum import Enum


class DeviceThreatProtectionLevel(Enum):
    unavailable = "0"
    secured = "1"
    low = "2"
    medium = "3"
    high = "4"
    notSet = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DeviceThreatProtectionLevel"
