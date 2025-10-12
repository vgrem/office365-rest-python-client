from office365.runtime.client_value import ClientValue


class SecondaryAdministratorsInfo(ClientValue):

    def __init__(
        self,
        email=None,
        loginName=None,
        userPrincipalName=None,
        login_name: str = None,
        name: str = None,
        user_principal_name: str = None,
    ):
        """

        :param str email:
        :param str loginName:
        :param str userPrincipalName:
        """
        super().__init__()
        self.email = email
        self.loginName = loginName
        self.userPrincipalName = userPrincipalName
        self.loginName = login_name
        self.name = name
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.SecondaryAdministratorsInfo"
