from enum import Enum


class DestinationType(Enum):
    new = "0"
    inPlace = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DestinationType"
