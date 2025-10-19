from enum import Enum


class ScopeOperatorType(Enum):
    Binary = "0"
    Unary = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ScopeOperatorType"
