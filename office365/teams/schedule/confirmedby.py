from enum import Enum


class ConfirmedBy(Enum):
    none = "0"
    user = "1"
    manager = "2"
    unknownFutureValue = "1024"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ConfirmedBy"
