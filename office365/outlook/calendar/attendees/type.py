from enum import Enum


class AttendeeType(Enum):
    required = "0"
    optional = "1"
    resource = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AttendeeType"
