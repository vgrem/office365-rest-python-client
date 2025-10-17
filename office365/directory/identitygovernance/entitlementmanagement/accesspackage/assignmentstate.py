from enum import Enum


class AccessPackageAssignmentState(Enum):
    delivering = "0"
    partiallyDelivered = "1"
    delivered = "2"
    expired = "3"
    deliveryFailed = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageAssignmentState"
