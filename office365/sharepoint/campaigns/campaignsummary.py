from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.campaigns.userinfo import CampaignUserInfo


class CampaignSummary(ClientValue):

    def __init__(
        self,
        campaign_id: str = None,
        end_date: datetime = None,
        owner: CampaignUserInfo = CampaignUserInfo(),
        start_date: datetime = None,
        status: str = None,
        tags: StringCollection = StringCollection(),
        title: str = None,
    ):
        self.campaignId = campaign_id
        self.endDate = end_date
        self.owner = owner
        self.startDate = start_date
        self.status = status
        self.tags = tags
        self.title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignSummary"
