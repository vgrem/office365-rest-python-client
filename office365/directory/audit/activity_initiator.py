from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.applications.app_identity import AppIdentity
from office365.runtime.client_value import ClientValue


@dataclass
class AuditActivityInitiator(ClientValue):
    """Identity the resource object that initiates the activity.
    The initiator can be a user, an app, or a system (which is considered an app).

    Args:
        app (AppIdentity): If the resource initiating the activity is an app, this property indicates all
          the app related information like appId, Name, servicePrincipalId, Name.
        user (AppIdentity): If the resource initiating the activity is a user, this property Indicates all the user
          related information like userId, Name, UserPrinicpalName.
    """

    app: AppIdentity = field(default_factory=AppIdentity)
    user: AppIdentity = field(default_factory=AppIdentity)

    @property
    def user_principal_name(self) -> str:
        """The user principal name if this is a user-initiated activity."""
        return getattr(self.user, "userPrincipalName", None) or ""

    def __str__(self) -> str:
        return self.user_principal_name or str(self.user) or str(self.app) or "Unknown"

    @property
    def entity_type_name(self):
        return "microsoft.graph.AuditActivityInitiator"
