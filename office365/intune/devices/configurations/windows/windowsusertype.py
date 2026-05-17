from enum import Enum


class WindowsUserType(Enum):
    administrator = "0"
    standard = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WindowsUserType"
