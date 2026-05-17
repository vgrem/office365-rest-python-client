from enum import Enum


class PrintScaling(Enum):
    auto = "0"
    shrinkToFit = "1"
    fill = "2"
    fit = "3"
    none = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintScaling"
