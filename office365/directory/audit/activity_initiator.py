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
    def entity_type_name(self):
        return "microsoft.graph.AuditActivityInitiator"
