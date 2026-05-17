from enum import Enum


class ManagementState(Enum):
    managed = "0"
    retirePending = "1"
    retireFailed = "2"
    wipePending = "3"
    wipeFailed = "4"
    unhealthy = "5"
    deletePending = "6"
    retireIssued = "7"
    wipeIssued = "8"
    wipeCanceled = "9"
    retireCanceled = "10"
    discovered = "11"
    unknownFutureValue = "12"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ManagementState"
