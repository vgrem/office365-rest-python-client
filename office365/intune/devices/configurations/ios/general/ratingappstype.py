from enum import Enum


class RatingAppsType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    agesAbove4 = "2"
    agesAbove9 = "3"
    agesAbove12 = "4"
    agesAbove17 = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingAppsType"
