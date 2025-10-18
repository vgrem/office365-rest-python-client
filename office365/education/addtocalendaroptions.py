from enum import Enum


class EducationAddToCalendarOptions(Enum):
    none = "0"
    studentsAndPublisher = "1"
    studentsAndTeamOwners = "2"
    unknownFutureValue = "3"
    studentsOnly = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.EducationAddToCalendarOptions"
