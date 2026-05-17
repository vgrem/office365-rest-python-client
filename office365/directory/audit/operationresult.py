from enum import Enum


class OperationResult(Enum):
    success = "0"
    failure = "1"
    timeout = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OperationResult"
