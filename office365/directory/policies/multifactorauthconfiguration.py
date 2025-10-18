from enum import Enum


class MultiFactorAuthConfiguration(Enum):
    notRequired = "0"
    required = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MultiFactorAuthConfiguration"
