from enum import Enum


class ExecutionMode(Enum):
    evaluateInline = "1"
    evaluateOffline = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ExecutionMode"
