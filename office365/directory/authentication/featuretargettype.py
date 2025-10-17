from enum import Enum


class FeatureTargetType(Enum):
    group = "0"
    administrativeUnit = "1"
    role = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.FeatureTargetType"
