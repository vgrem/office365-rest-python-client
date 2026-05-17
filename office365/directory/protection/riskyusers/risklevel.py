from enum import Enum


class RiskLevel(Enum):
    low = "0"
    medium = "1"
    high = "2"
    hidden = "3"
    none = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RiskLevel"
