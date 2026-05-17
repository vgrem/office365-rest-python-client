from enum import Enum


class ScheduleEntityTheme(Enum):
    white = "0"
    blue = "1"
    green = "2"
    purple = "3"
    pink = "4"
    yellow = "5"
    gray = "6"
    darkBlue = "7"
    darkGreen = "8"
    darkPurple = "9"
    darkPink = "10"
    darkYellow = "11"
    unknownFutureValue = "12"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ScheduleEntityTheme"
