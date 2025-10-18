from enum import Enum


class LayoutTemplateType(Enum):
    default = "0"
    verticalSplit = "1"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.LayoutTemplateType"
