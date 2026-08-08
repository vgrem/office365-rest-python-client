from enum import Enum


class AccessPackageAssignmentRequestFilterByCurrentUserOptions(Enum):
    target = "1"
    createdBy = "2"
    approver = "3"
    unknownFutureValue = "99"
    targetOrRequestor = "100"
    targetManager = "101"
    requestForOthers = "102"
    targetAgentIdentitySponsorOrOwner = "103"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageAssignmentRequestFilterByCurrentUserOptions"
