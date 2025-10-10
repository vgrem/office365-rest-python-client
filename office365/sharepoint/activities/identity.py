from office365.runtime.client_value import ClientValue
from office365.sharepoint.activities.identity_item import ActivityIdentityItem


class ActivityIdentity(ClientValue):

    def __init__(
        self,
        client_id=None,
        group=ActivityIdentityItem(),
        user=ActivityIdentityItem(),
        client_id_provider: str = None,
        email: str = None,
        name: str = None,
        user_principal_name: str = None,
    ):
        """
        :param str client_id:
        """
        self.clientId = client_id
        self.group = group
        self.user = user
        self.clientIdProvider = client_id_provider
        self.email = email
        self.name = name
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.ActivityIdentity"
