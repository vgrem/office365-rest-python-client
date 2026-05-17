from enum import Enum


class AttributeFlowType(Enum):
    Always = "0"
    ObjectAddOnly = "1"
    MultiValueAddOnly = "2"
    ValueAddOnly = "3"
    AttributeAddOnly = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttributeFlowType"
