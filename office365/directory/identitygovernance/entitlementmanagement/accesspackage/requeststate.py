from enum import Enum


class AccessPackageRequestState(Enum):
    submitted = "0"
    pendingApproval = "1"
    delivering = "2"
    delivered = "3"
    deliveryFailed = "4"
    denied = "5"
    scheduled = "6"
    canceled = "7"
    partiallyDelivered = "8"
    unknownFutureValue = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageRequestState"
