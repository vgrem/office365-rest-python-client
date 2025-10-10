from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.user_info import UserInfo


class SiteUserGroupsData(ClientValue):

    def __init__(
        self,
        members: ClientValueCollection[UserInfo] = ClientValueCollection(UserInfo),
        owners: ClientValueCollection[UserInfo] = ClientValueCollection(UserInfo),
        site_id: UUID = None,
        visitors: ClientValueCollection[UserInfo] = ClientValueCollection(UserInfo),
    ):
        self.members = members
        self.owners = owners
        self.siteId = site_id
        self.visitors = visitors

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteUserGroupsData"
