from enum import Enum


class RatingAustraliaMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    mature = "4"
    agesAbove15 = "5"
    agesAbove18 = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingAustraliaMoviesType"
