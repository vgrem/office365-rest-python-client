from enum import Enum


class ProtectionSource(Enum):
    none = "0"
    manual = "1"
    dynamicRule = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ProtectionSource"
