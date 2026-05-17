from enum import Enum


class EscrowBehavior(Enum):
    Default = "1"
    IgnoreLookupReferenceResolutionFailure = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EscrowBehavior"
