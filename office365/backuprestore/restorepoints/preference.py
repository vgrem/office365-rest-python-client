from enum import Enum


class RestorePointPreference(Enum):
    latest = "0"
    oldest = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RestorePointPreference"
