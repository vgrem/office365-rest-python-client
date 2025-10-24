from enum import Enum


class PrintMultipageLayout(Enum):
    clockwiseFromTopLeft = "0"
    counterclockwiseFromTopLeft = "1"
    counterclockwiseFromTopRight = "2"
    clockwiseFromTopRight = "3"
    counterclockwiseFromBottomLeft = "4"
    clockwiseFromBottomLeft = "5"
    counterclockwiseFromBottomRight = "6"
    clockwiseFromBottomRight = "7"
    unknownFutureValue = "8"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintMultipageLayout"
