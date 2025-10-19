from enum import Enum


class RatingNewZealandTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    adults = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingNewZealandTelevisionType"
