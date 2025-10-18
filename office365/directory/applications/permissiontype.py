from enum import Enum


class PermissionType(Enum):
    application = "3"
    delegated = "2"
    delegatedUserConsentable = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.PermissionType"
