from enum import Enum


class ExpirationPatternType(Enum):
    notSpecified = "0"
    noExpiration = "1"
    afterDateTime = "2"
    afterDuration = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ExpirationPatternType"
