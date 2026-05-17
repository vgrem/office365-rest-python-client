from enum import Enum


class RejectReason(Enum):
    none = "0"
    busy = "1"
    forbidden = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RejectReason"
