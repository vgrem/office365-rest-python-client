from enum import Enum


class ScopeOperatorMultiValuedComparisonType(Enum):
    All = "0"
    Any = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ScopeOperatorMultiValuedComparisonType"
