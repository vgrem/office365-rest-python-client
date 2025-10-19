from enum import Enum


class InternetSiteSecurityLevel(Enum):
    userDefined = "0"
    medium = "1"
    mediumHigh = "2"
    high = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.InternetSiteSecurityLevel"
