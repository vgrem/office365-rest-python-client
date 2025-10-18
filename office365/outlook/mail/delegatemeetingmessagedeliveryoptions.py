from enum import Enum


class DelegateMeetingMessageDeliveryOptions(Enum):
    sendToDelegateAndInformationToPrincipal = "0"
    sendToDelegateAndPrincipal = "1"
    sendToDelegateOnly = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegateMeetingMessageDeliveryOptions"
