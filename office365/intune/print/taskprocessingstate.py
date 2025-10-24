from enum import Enum


class PrintTaskProcessingState(Enum):
    pending = "0"
    processing = "1"
    completed = "2"
    aborted = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintTaskProcessingState"
