from office365.runtime.client_value import ClientValue


class ActivityIdentityItem(ClientValue):
    def __init__(
        self,
        client_id=None,
        clientIdProvider=None,
        displayName=None,
        email=None,
        userPrincipalName=None,
        client_id_provider: str = None,
        display_name: str = None,
        user_principal_name: str = None,
    ):
        """
        :param str client_id:
        :param str clientIdProvider:
        :param str displayName:
        :param str email:
        :param str userPrincipalName:
        """
        self.clientId = client_id
        self.clientIdProvider = clientIdProvider
        self.displayName = displayName
        self.email = email
        self.userPrincipalName = userPrincipalName
        self.clientIdProvider = client_id_provider
        self.displayName = display_name
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityIdentityItem"
