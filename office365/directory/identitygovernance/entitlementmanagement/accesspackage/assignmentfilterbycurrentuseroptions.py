from enum import Enum


class AccessPackageAssignmentFilterByCurrentUserOptions(Enum):
    target = "1"
    createdBy = "2"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageAssignmentFilterByCurrentUserOptions"
