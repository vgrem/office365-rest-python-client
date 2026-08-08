from enum import Enum


class RestoreJobType(Enum):
    standard = "0"
    bulk = "1"
    unknownFutureValue = "2"
    granular = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RestoreJobType"
