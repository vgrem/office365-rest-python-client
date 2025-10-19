from enum import Enum


class RatingUnitedStatesMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    parentalGuidance13 = "4"
    restricted = "5"
    adults = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingUnitedStatesMoviesType"
