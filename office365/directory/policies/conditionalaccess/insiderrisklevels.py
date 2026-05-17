from enum import Enum


class ConditionalAccessInsiderRiskLevels(Enum):
    minor = "1"
    moderate = "2"
    elevated = "4"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessInsiderRiskLevels"
