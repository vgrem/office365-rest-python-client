from enum import Enum


class IdentityUserFlowAttributeType(Enum):
    builtIn = "1"
    custom = "2"
    required = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.IdentityUserFlowAttributeType"
