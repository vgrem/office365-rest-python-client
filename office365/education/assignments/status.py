from enum import Enum


class EducationAssignmentStatus(Enum):
    draft = "0"
    published = "1"
    assigned = "2"
    unknownFutureValue = "3"
    inactive = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationAssignmentStatus"
