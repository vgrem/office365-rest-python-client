from enum import Enum


class WeakAlgorithms(Enum):
    rsaSha1 = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.WeakAlgorithms"
