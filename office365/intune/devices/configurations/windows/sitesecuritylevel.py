from enum import Enum


class SiteSecurityLevel(Enum):
    userDefined = "0"
    low = "1"
    mediumLow = "2"
    medium = "3"
    mediumHigh = "4"
    high = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SiteSecurityLevel"
