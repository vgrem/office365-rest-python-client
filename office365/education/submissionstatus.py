from enum import Enum


class EducationSubmissionStatus(Enum):
    working = "0"
    submitted = "1"
    released = "2"
    returned = "3"
    unknownFutureValue = "4"
    reassigned = "5"
    excused = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationSubmissionStatus"
