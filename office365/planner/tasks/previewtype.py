from enum import Enum


class PlannerPreviewType(Enum):
    automatic = "0"
    noPreview = "1"
    checklist = "2"
    description = "3"
    reference = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PlannerPreviewType"
