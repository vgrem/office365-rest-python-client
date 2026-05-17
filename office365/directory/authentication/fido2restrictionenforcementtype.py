from enum import Enum


class Fido2RestrictionEnforcementType(Enum):
    allow = "0"
    block = "1"
    unknownFutureValue = "2"

    none = "-1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.Fido2RestrictionEnforcementType"
