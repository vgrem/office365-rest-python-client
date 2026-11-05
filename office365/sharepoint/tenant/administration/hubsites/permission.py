from __future__ import annotations

from office365.runtime.client_value import ClientValue


class HubSitePermission(ClientValue):
    """Args:
    display_name (str):
    principal_name (str):
    rights (int):
    """

    DisplayName: str | None = None
    PrincipalName: str | None = None
    Rights: int | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.HubSitePermission"
