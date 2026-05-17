from enum import Enum


class RatingIrelandMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    agesAbove12 = "4"
    agesAbove15 = "5"
    agesAbove16 = "6"
    adults = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingIrelandMoviesType"
