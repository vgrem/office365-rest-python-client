from enum import Enum


class PrintJobProcessingState(Enum):
    unknown = "0"
    pending = "1"
    processing = "2"
    paused = "3"
    stopped = "4"
    completed = "5"
    canceled = "6"
    aborted = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintJobProcessingState"
