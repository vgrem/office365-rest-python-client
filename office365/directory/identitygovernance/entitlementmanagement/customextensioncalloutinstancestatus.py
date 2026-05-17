from enum import Enum


class CustomExtensionCalloutInstanceStatus(Enum):
    calloutSent = "1"
    callbackReceived = "2"
    calloutFailed = "3"
    callbackTimedOut = "4"
    waitingForCallback = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CustomExtensionCalloutInstanceStatus"
