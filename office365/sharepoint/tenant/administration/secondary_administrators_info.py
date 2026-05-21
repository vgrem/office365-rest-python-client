from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SecondaryAdministratorsInfo(ClientValue):
    """
    :param str email:
    :param str login_name:
    :param str name:
    :param str user_principal_name:
    """

    email: str | None = None
    loginName: str | None = None
    name: str | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsInfo"
