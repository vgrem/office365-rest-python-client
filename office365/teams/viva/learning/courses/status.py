from enum import Enum


class CourseStatus(Enum):
    notStarted = "0"
    inProgress = "1"
    completed = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CourseStatus"
