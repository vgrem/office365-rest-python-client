from enum import Enum


class CalendarSharingAction(Enum):
    """"""

    accept = "0"
    acceptAndViewCalendar = "1"
    viewCalendar = "2"
    addThisCalendar = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CalendarSharingAction"
