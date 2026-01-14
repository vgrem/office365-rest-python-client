from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.campaigns.userinfo import CampaignUserInfo


class CampaignEntity(ClientValue):
    def __init__(
        self,
        campaign_id: str = None,
        channels: StringCollection = None,
        contributors: ClientValueCollection[CampaignUserInfo] = ClientValueCollection(CampaignUserInfo),
        description: str = None,
        end_date: datetime = None,
        objectives: StringCollection = None,
        owner: CampaignUserInfo = CampaignUserInfo(),
        start_date: datetime = None,
        status: str = None,
        tags: StringCollection = StringCollection(),
        title: str = None,
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
