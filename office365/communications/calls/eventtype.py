from enum import Enum


class CallEventType(Enum):
    callStarted = "0"
    callEnded = "1"
    unknownFutureValue = "2"
    rosterUpdated = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CallEventType"
