from enum import Enum


class AccessPackageAssignmentFilterByCurrentUserOptions(Enum):
    target = "1"
    createdBy = "2"
    unknownFutureValue = "99"
    targetManager = "100"
    targetAgentIdentitySponsorOrOwner = "101"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageAssignmentFilterByCurrentUserOptions"
