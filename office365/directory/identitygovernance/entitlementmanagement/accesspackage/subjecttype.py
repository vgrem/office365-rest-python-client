from enum import Enum


class AccessPackageSubjectType(Enum):
    notSpecified = "0"
    user = "1"
    servicePrincipal = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageSubjectType"
