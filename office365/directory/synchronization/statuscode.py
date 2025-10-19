from enum import Enum


class SynchronizationStatusCode(Enum):
    NotConfigured = "0"
    NotRun = "1"
    Active = "2"
    Paused = "3"
    Quarantine = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SynchronizationStatusCode"
