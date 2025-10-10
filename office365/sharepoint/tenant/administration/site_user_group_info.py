from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.user_info import UserInfo


class SiteUserGroupInfo(ClientValue):

    def __init__(
        self,
        user_group: ClientValueCollection[UserInfo] = ClientValueCollection(UserInfo),
    ):
        self.userGroup = user_group

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteUserGroupInfo"
