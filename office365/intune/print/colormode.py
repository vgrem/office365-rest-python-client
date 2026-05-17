from enum import Enum


class PrintColorMode(Enum):
    blackAndWhite = "0"
    grayscale = "1"
    color = "2"
    auto = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintColorMode"
