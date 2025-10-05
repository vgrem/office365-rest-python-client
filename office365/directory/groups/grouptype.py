from enum import Enum


class GroupType(Enum):
    unifiedGroups = "0"
    azureAD = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.GroupType"
