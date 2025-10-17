from enum import Enum


class RiskState(Enum):
    none = "0"
    confirmedSafe = "1"
    remediated = "2"
    dismissed = "3"
    atRisk = "4"
    confirmedCompromised = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RiskState"
