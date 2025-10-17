from enum import Enum


class DataSubjectType(Enum):
    customer = "0"
    currentEmployee = "1"
    formerEmployee = "2"
    prospectiveEmployee = "3"
    student = "4"
    teacher = "5"
    faculty = "6"
    other = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DataSubjectType"
