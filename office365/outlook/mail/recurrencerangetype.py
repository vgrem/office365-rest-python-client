from enum import Enum


class RecurrenceRangeType(Enum):
    endDate = "0"
    noEnd = "1"
    numbered = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RecurrenceRangeType"
