from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ActivityIdentityItem(ClientValue):
    """
    :param str client_id:
    :param str clientIdProvider:
    :param str displayName:
    :param str email:
    :param str userPrincipalName:
    """

    clientId: str | None = None
    clientIdProvider: str | None = None
    displayName: str | None = None
    email: str | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityIdentityItem"
