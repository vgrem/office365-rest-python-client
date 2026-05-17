from enum import Enum


class ConditionalAccessStatus(Enum):
    success = "0"
    failure = "1"
    notApplied = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConditionalAccessStatus"
