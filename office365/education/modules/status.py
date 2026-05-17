from enum import Enum


class EducationModuleStatus(Enum):
    draft = "0"
    published = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationModuleStatus"
