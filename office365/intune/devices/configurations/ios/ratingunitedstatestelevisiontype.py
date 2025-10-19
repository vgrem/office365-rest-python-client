from enum import Enum


class RatingUnitedStatesTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    childrenAll = "2"
    childrenAbove7 = "3"
    general = "4"
    parentalGuidance = "5"
    childrenAbove14 = "6"
    adults = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingUnitedStatesTelevisionType"
