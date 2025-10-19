from enum import Enum


class AttributeType(Enum):
    String = "0"
    Integer = "1"
    Reference = "2"
    Binary = "3"
    Boolean = "4"
    DateTime = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttributeType"
