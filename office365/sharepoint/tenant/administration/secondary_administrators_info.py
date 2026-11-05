from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SecondaryAdministratorsInfo(ClientValue):
    email: str | None = None
    loginName: str | None = None
    name: str | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsInfo"
