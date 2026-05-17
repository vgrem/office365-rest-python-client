from enum import Enum


class InsiderRiskLevel(Enum):
    none = "0"
    minor = "1"
    moderate = "2"
    elevated = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.InsiderRiskLevel"
