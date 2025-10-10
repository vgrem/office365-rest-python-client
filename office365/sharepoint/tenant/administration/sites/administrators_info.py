from office365.runtime.client_value import ClientValue


class SiteAdministratorsInfo(ClientValue):

    def __init__(
        self, email=None, login_name=None, name=None, user_principal_name: str = None
    ):
        """
        :param str email:
        :param str login_name:
        :param str name:
        """
        self.email = email
        self.loginName = login_name
        self.name = name
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteAdministratorsInfo"
