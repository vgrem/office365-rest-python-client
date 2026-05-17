from enum import Enum


class RestoreSessionStatus(Enum):
    draft = "0"
    activating = "1"
    active = "2"
    completedWithError = "3"
    completed = "4"
    unknownFutureValue = "5"
    failed = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RestoreSessionStatus"
