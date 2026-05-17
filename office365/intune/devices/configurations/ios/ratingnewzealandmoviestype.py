from enum import Enum


class RatingNewZealandMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    parentalGuidance = "3"
    mature = "4"
    agesAbove13 = "5"
    agesAbove15 = "6"
    agesAbove16 = "7"
    agesAbove18 = "8"
    restricted = "9"
    agesAbove16Restricted = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingNewZealandMoviesType"
