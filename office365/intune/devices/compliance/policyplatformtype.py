from enum import Enum


class PolicyPlatformType(Enum):
    android = "0"
    androidForWork = "1"
    iOS = "2"
    macOS = "3"
    windowsPhone81 = "4"
    windows81AndLater = "5"
    windows10AndLater = "6"
    all = "100"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PolicyPlatformType"
