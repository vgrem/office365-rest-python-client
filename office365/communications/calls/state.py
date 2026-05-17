from enum import Enum


class CallState(Enum):
    incoming = "0"
    establishing = "1"
    established = "3"
    hold = "4"
    transferring = "5"
    transferAccepted = "6"
    redirecting = "7"
    terminating = "8"
    terminated = "9"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CallState"
