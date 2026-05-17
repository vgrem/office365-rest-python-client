from enum import Enum


class AccessPackageExternalUserLifecycleAction(Enum):
    none = "0"
    blockSignIn = "1"
    blockSignInAndDelete = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AccessPackageExternalUserLifecycleAction"
