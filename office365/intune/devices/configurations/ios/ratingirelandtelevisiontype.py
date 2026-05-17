from enum import Enum


class RatingIrelandTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    children = "3"
    youngAdults = "4"
    parentalSupervision = "5"
    mature = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingIrelandTelevisionType"
