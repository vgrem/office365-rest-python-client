from enum import Enum


class DayOfWeek(Enum):
    sunday = "0"
    monday = "1"
    tuesday = "2"
    wednesday = "3"
    thursday = "4"
    friday = "5"
    saturday = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DayOfWeek"
