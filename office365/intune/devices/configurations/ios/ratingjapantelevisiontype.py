from enum import Enum


class RatingJapanTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    explicitAllowed = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingJapanTelevisionType"
