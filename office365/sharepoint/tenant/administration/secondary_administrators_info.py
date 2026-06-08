from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SecondaryAdministratorsInfo(ClientValue):
    """Args:
        email (str):
        login_name (str):
        name (str):
        user_principal_name (str):
    """

    email: str | None = None
    loginName: str | None = None
    name: str | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsInfo"
