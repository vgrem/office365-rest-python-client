from enum import Enum


class ScheduleChangeRequestActor(Enum):
    sender = "0"
    recipient = "1"
    manager = "2"
    system = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ScheduleChangeRequestActor"
