from enum import Enum


class EducationGender(Enum):
    female = "0"
    male = "1"
    other = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationGender"
