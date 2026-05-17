from enum import Enum


class SharingDomainRestrictionMode(Enum):
    none = "0"
    allowList = "1"
    blockList = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SharingDomainRestrictionMode"
