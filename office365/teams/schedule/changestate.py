from enum import Enum


class ScheduleChangeState(Enum):
    pending = "0"
    approved = "1"
    declined = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ScheduleChangeState"
