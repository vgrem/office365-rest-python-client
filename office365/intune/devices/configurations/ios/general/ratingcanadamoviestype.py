from enum import Enum


class RatingCanadaMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    agesAbove14 = "4"
    agesAbove18 = "5"
    restricted = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingCanadaMoviesType"
