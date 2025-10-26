from enum import Enum


class ConnectionOperationStatus(Enum):
    unspecified = "0"
    inprogress = "1"
    completed = "2"
    failed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.externalConnectors.ConnectionOperationStatus"
