from enum import Enum


class RestoreJobType(Enum):
    standard = "0"
    bulk = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RestoreJobType"
