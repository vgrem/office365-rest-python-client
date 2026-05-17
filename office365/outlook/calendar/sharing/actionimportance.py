from enum import Enum


class CalendarSharingActionImportance(Enum):
    primary = "0"
    secondary = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.CalendarSharingActionImportance"
