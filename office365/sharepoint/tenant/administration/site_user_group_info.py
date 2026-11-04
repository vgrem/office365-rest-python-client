from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.sharepoint.publishing.user_info import UserInfo


@value
class SiteUserGroupInfo(ClientValue):
    userGroup: ClientValueCollection[UserInfo] = field(default_factory=lambda: ClientValueCollection(UserInfo))

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SiteUserGroupInfo"
