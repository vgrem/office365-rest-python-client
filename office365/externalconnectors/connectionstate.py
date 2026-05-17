from enum import Enum


class ConnectionState(Enum):
    draft = "1"
    ready = "2"
    obsolete = "3"
    limitExceeded = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.externalConnectors.ConnectionState"
