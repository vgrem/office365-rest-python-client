from enum import Enum


class RatingCanadaTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    children = "2"
    childrenAbove8 = "3"
    general = "4"
    parentalGuidance = "5"
    agesAbove14 = "6"
    agesAbove18 = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingCanadaTelevisionType"
