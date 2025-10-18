from enum import Enum


class CalendarSharingActionType(Enum):
    accept = "0"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CalendarSharingActionType"
