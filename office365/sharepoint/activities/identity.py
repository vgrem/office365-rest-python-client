from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.activities.identity_item import ActivityIdentityItem


@dataclass
class ActivityIdentity(ClientValue):
    clientId: Optional[str] = None
    group: ActivityIdentityItem = field(default_factory=ActivityIdentityItem)
    user: ActivityIdentityItem = field(default_factory=ActivityIdentityItem)
    clientIdProvider: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    userPrincipalName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityIdentity"
