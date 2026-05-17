from enum import Enum


class WeekIndex(Enum):
    first = "0"
    second = "1"
    third = "2"
    fourth = "3"
    last = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WeekIndex"
