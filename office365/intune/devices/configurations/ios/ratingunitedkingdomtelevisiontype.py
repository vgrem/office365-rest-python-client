from enum import Enum


class RatingUnitedKingdomTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    caution = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingUnitedKingdomTelevisionType"
