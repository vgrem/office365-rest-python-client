from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SiteAdministratorsInfo(ClientValue):
    """Args:
    email (str):
    login_name (str):
    name (str):
    """

    userPrincipalName: str | None = None
    email: str | None = None
    loginName: str | None = None
    name: str | None = None

    def __str__(self):
        return self.name or self.entity_type_name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsInfo"
