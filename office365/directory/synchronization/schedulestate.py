from enum import Enum


class SynchronizationScheduleState(Enum):
    Active = "0"
    Disabled = "1"
    Paused = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SynchronizationScheduleState"
