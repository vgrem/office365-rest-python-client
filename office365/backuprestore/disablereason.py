from enum import Enum


class DisableReason(Enum):
    none = "0"
    invalidBillingProfile = "1"
    userRequested = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DisableReason"
