from enum import Enum


class WeeklySchedule(Enum):
    userDefined = "0"
    everyday = "1"
    sunday = "2"
    monday = "3"
    tuesday = "4"
    wednesday = "5"
    thursday = "6"
    friday = "7"
    saturday = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WeeklySchedule"
