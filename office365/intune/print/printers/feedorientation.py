from enum import Enum


class PrinterFeedOrientation(Enum):
    longEdgeFirst = "0"
    shortEdgeFirst = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrinterFeedOrientation"
