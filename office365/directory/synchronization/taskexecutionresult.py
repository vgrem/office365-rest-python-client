from enum import Enum


class SynchronizationTaskExecutionResult(Enum):
    Succeeded = "0"
    Failed = "1"
    EntryLevelErrors = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.SynchronizationTaskExecutionResult"
