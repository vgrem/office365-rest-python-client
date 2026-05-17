from enum import Enum


class PrintOrientation(Enum):
    portrait = "3"
    landscape = "4"
    reverseLandscape = "5"
    reversePortrait = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PrintOrientation"
