from enum import Enum


class AccessType(Enum):
    grant = "1"
    deny = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.externalConnectors.AccessType"
