from enum import Enum


class CallDirection(Enum):
    incoming = "0"
    outgoing = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CallDirection"
