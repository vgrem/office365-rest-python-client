from enum import Enum


class CalendarColor(Enum):
    auto = "-1"
    lightBlue = "0"
    lightGreen = "1"
    lightOrange = "2"
    lightGray = "3"
    lightYellow = "4"
    lightTeal = "5"
    lightPink = "6"
    lightBrown = "7"
    lightRed = "8"
    maxColor = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CalendarColor"
