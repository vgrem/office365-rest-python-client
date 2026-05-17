from enum import Enum


class RecipientScopeType(Enum):
    none = "0"
    internal = "1"
    external = "2"
    externalPartner = "4"
    externalNonPartner = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RecipientScopeType"
