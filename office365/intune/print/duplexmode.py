from enum import Enum


class PrintDuplexMode(Enum):
    flipOnLongEdge = "0"
    flipOnShortEdge = "1"
    oneSided = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintDuplexMode"
