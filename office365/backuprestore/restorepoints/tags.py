from enum import Enum


class RestorePointTags(Enum):
    none = "0"
    fastRestore = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RestorePointTags"
