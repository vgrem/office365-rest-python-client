from enum import Enum


class RatingAustraliaTelevisionType(Enum):
    allAllowed = "0"
    allBlocked = "1"
    preschoolers = "2"
    children = "3"
    general = "4"
    parentalGuidance = "5"
    mature = "6"
    agesAbove15 = "7"
    agesAbove15AdultViolence = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RatingAustraliaTelevisionType"
