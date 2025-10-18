from enum import Enum


class LabelActionSource(Enum):
    manual = "0"
    automatic = "1"
    recommended = "2"
    none = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.LabelActionSource"
