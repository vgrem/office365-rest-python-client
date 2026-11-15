from enum import Enum


class TeamworkTagType(Enum):
    standard = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamworkTagType"
