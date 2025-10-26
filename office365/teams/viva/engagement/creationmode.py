from enum import Enum


class EngagementCreationMode(Enum):
    none = "0"
    migration = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EngagementCreationMode"
