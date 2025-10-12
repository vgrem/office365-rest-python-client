from enum import Enum


class IncludedUserTypes(Enum):
    all = "0"
    member = "1"
    guest = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IncludedUserTypes"
