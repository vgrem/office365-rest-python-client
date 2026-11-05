from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ActivityIdentityItem(ClientValue):
    """Args:
    client_id (str):
    clientIdProvider (str):
    displayName (str):
    email (str):
    userPrincipalName (str):
    """

    clientId: str | None = None
    clientIdProvider: str | None = None
    displayName: str | None = None
    email: str | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityIdentityItem"
