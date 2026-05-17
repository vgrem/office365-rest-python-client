from enum import Enum


class RecurrencePatternType(Enum):
    daily = "0"
    weekly = "1"
    absoluteMonthly = "2"
    relativeMonthly = "3"
    absoluteYearly = "4"
    relativeYearly = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RecurrencePatternType"
