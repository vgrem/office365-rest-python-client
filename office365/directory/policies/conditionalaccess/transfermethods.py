from enum import Enum


class ConditionalAccessTransferMethods(Enum):
    none = "0"
    deviceCodeFlow = "1"
    authenticationTransfer = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessTransferMethods"
