from enum import Enum


class RatingFranceTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    agesAbove10 = "2"
    agesAbove12 = "3"
    agesAbove16 = "4"
    agesAbove18 = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingFranceTelevisionType"
