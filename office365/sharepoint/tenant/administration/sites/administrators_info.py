from office365.runtime.client_value import ClientValue
from typing import Optional


class SiteAdministratorsInfo(ClientValue):
    def __init__(self, email=None, login_name=None, name=None, user_principal_name: Optional[str] = None):
        """
        :param str email:
        :param str login_name:
        :param str name:
        """
        self.email = email
        self.loginName = login_name
        self.name = name
        self.userPrincipalName = user_principal_name

    def __str__(self):
        return self.name or self.entity_type_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsInfo"
