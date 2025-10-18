from enum import Enum


class EducationAddedStudentAction(Enum):
    none = "0"
    assignIfOpen = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationAddedStudentAction"
