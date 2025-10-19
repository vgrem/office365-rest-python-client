from enum import Enum


class SafeSearchFilterType(Enum):
    userDefined = "0"
    strict = "1"
    moderate = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SafeSearchFilterType"
