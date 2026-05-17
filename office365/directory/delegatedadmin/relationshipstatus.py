from enum import Enum


class DelegatedAdminRelationshipStatus(Enum):
    activating = "0"
    active = "1"
    approvalPending = "2"
    approved = "3"
    created = "4"
    expired = "5"
    expiring = "6"
    terminated = "7"
    terminating = "8"
    terminationRequested = "9"
    unknownFutureValue = "10"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegatedAdminRelationshipStatus"
