from enum import Enum


class RatingGermanyTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    agesAbove6 = "3"
    agesAbove12 = "4"
    agesAbove16 = "5"
    adults = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingGermanyTelevisionType"
