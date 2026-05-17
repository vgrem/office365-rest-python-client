from enum import Enum


class AgreementAcceptanceState(Enum):
    accepted = "2"
    declined = "3"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AgreementAcceptanceState"
