from enum import Enum


class RatingUnitedKingdomMoviesType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    general = "2"
    universalChildren = "3"
    parentalGuidance = "4"
    agesAbove12Video = "5"
    agesAbove12Cinema = "6"
    agesAbove15 = "7"
    adults = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingUnitedKingdomMoviesType"
