from enum import Enum


class AccessPackageFilterByCurrentUserOptions(Enum):
    allowedRequestor = "1"
    unknownFutureValue = "99"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageFilterByCurrentUserOptions"
