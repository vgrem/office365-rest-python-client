from enum import Enum


class FeatureType(Enum):
    registration = "0"
    reset = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FeatureType"
