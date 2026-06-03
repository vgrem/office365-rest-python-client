from typing import Optional

from office365.directory.identitygovernance.privilegedaccess.approval import Approval
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class UserConsentRequest(Entity):
    """
    Represents the details of the consent request a user creates when they request to access an app or to grant
    permissions to an app. The details include justification for requesting access, the status of the request,
    and the approval details.

    The user can create a consent request when an app or a permission requires admin authorization and only when the
    admin consent workflow is enabled.
    """

    @property
    def reason(self) -> Optional[str]:
        """Gets the reason property"""
        return self.properties.get("reason", None)

    @property
    def approval(self) -> Approval:
        """Gets the approval property"""
        return self.properties.get("approval", Approval(self.context, ResourcePath("approval", self.resource_path)))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserConsentRequest"
