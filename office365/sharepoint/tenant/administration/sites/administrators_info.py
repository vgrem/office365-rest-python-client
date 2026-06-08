from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SiteAdministratorsInfo(ClientValue):
    """Args:
    email (str):
    login_name (str):
    name (str):
    """

    email = None
    loginName = None
    name = None
    userPrincipalName: str | None = None

    def __str__(self):
        return self.name or self.entity_type_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsInfo"
