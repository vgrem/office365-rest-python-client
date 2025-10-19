from enum import Enum


class AttributeFlowBehavior(Enum):
    FlowWhenChanged = "0"
    FlowAlways = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttributeFlowBehavior"
