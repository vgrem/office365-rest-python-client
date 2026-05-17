from enum import Enum


class PrintEvent(Enum):
    jobStarted = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintEvent"
