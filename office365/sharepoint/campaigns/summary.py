from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.campaigns.userinfo import CampaignUserInfo


@dataclass
class CampaignSummary(ClientValue):
    campaignId: Optional[str] = None
    endDate: Optional[datetime] = None
    owner: CampaignUserInfo = field(default_factory=CampaignUserInfo)
    startDate: Optional[datetime] = None
    status: Optional[str] = None
    tags: StringCollection = field(default_factory=StringCollection)
    title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignSummary"
