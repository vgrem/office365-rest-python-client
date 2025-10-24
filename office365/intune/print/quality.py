from enum import Enum


class PrintQuality(Enum):
    low = "0"
    medium = "1"
    high = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintQuality"
