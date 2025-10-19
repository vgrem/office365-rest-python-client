from enum import Enum


class EdgeCookiePolicy(Enum):
    userDefined = "0"
    allow = "1"
    blockThirdParty = "2"
    blockAll = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EdgeCookiePolicy"
