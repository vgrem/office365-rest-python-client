from enum import Enum


class ConditionalAccessDevicePlatform(Enum):
    android = "0"
    iOS = "1"
    windows = "2"
    windowsPhone = "3"
    macOS = "4"
    all = "5"
    unknownFutureValue = "6"
    linux = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessDevicePlatform"
