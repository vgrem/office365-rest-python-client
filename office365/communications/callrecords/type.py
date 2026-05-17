from enum import Enum


class CallType(Enum):
    unknown = "0"
    groupCall = "1"
    peerToPeer = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.callRecords.CallType"
