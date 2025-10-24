from enum import Enum


class OnlineMeetingRole(Enum):
    attendee = "0"
    presenter = "1"
    unknownFutureValue = "2"
    producer = "3"
    coorganizer = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnlineMeetingRole"
