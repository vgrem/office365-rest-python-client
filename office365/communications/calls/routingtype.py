from enum import Enum


class RoutingType(Enum):
    forwarded = "0"
    lookup = "1"
    selfFork = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RoutingType"
