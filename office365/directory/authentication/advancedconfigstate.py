from enum import Enum


class AdvancedConfigState(Enum):
    default = "0"
    enabled = "1"
    disabled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AdvancedConfigState"
