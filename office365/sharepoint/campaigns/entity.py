from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.campaigns.userinfo import CampaignUserInfo


class CampaignEntity(ClientValue):
    def __init__(
        self,
        campaign_id: Optional[str] = None,
        channels: Optional[StringCollection] = None,
        contributors: ClientValueCollection[CampaignUserInfo] = ClientValueCollection(CampaignUserInfo),
        description: Optional[str] = None,
        end_date: Optional[datetime] = None,
        objectives: Optional[StringCollection] = None,
        owner: CampaignUserInfo = CampaignUserInfo(),
        start_date: Optional[datetime] = None,
        status: Optional[str] = None,
        tags: StringCollection = StringCollection(),
        title: Optional[str] = None,
    ):
        self.campaignId = campaign_id
        self.channels = channels
        self.contributors = contributors
        self.description = description
        self.endDate = end_date
        self.objectives = objectives
        self.owner = owner
        self.startDate = start_date
        self.status = status
        self.tags = tags
        self.title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignEntity"
