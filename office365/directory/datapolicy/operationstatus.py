from enum import Enum


class DataPolicyOperationStatus(Enum):
    notStarted = "0"
    running = "1"
    complete = "2"
    failed = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DataPolicyOperationStatus"
