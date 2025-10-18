from enum import Enum


class TemplateApplicationLevel(Enum):
    none = "0"
    newPartners = "1"
    existingPartners = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TemplateApplicationLevel"
