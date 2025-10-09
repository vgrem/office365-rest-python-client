from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.users.id_info import UserIdInfo


class CampaignUserInfo(ClientValue):

    def __init__(
        self,
        email: str = None,
        id_: int = None,
        is_external: bool = None,
        login_name: str = None,
        name: str = None,
        principal_type: int = None,
        user_id: UserIdInfo = UserIdInfo(),
        user_principal_name: str = None,
    ):
        self.email = email
        self.id = id_
        self.isExternal = is_external
        self.loginName = login_name
        self.name = name
        self.principalType = principal_type
        self.userId = user_id
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignUserInfo"
