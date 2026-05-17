from enum import Enum


class EducationUserRole(Enum):
    student = "0"
    teacher = "1"
    none = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationUserRole"
