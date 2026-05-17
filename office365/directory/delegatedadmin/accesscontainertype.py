from enum import Enum


class DelegatedAdminAccessContainerType(Enum):
    securityGroup = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.DelegatedAdminAccessContainerType"
