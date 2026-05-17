from enum import Enum


class AccessPackageAssignmentRequestFilterByCurrentUserOptions(Enum):
    target = "1"
    createdBy = "2"
    approver = "3"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageAssignmentRequestFilterByCurrentUserOptions"
