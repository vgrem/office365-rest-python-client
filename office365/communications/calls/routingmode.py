from enum import Enum


class RoutingMode(Enum):
    oneToOne = "0"
    multicast = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RoutingMode"
