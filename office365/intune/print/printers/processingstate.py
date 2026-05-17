from enum import Enum


class PrinterProcessingState(Enum):
    unknown = "0"
    idle = "1"
    processing = "2"
    stopped = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrinterProcessingState"
