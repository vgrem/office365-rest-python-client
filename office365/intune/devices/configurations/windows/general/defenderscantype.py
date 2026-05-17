from enum import Enum


class DefenderScanType(Enum):
    userDefined = "0"
    disabled = "1"
    quick = "2"
    full = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DefenderScanType"
