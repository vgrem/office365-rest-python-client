from enum import Enum


class AttributeMappingSourceType(Enum):
    Attribute = "0"
    Constant = "1"
    Function = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttributeMappingSourceType"
