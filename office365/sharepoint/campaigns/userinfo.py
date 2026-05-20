from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.principal.users.id_info import UserIdInfo


@dataclass
class CampaignUserInfo(ClientValue):
    email: Optional[str] = None
    id: Optional[int] = None
    isExternal: Optional[bool] = None
    loginName: Optional[str] = None
    name: Optional[str] = None
    principalType: Optional[int] = None
    userId: UserIdInfo = field(default_factory=UserIdInfo)
    userPrincipalName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignUserInfo"
