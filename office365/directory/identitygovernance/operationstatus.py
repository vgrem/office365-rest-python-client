from enum import Enum


class OperationStatus(Enum):
    NotStarted = "0"
    Running = "1"
    Completed = "2"
    Failed = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OperationStatus"
