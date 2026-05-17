from enum import Enum


class RatingJapanMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    agesAbove15 = "4"
    agesAbove18 = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingJapanMoviesType"
