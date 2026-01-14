from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.campaigns.userinfo import CampaignUserInfo


class CampaignCommunicationEntity(ClientValue):
    def __init__(
        self,
        campaign_id: str = None,
        channels: StringCollection = StringCollection(),
        communication_id: str = None,
        created_by: CampaignUserInfo = CampaignUserInfo(),
        last_edited_date_time: datetime = None,
        page: str = None,
        publishing_date_time: datetime = None,
        state: str = None,
        title: str = None,
    ):
        self.campaignId = campaign_id
        self.channels = channels
        self.communicationId = communication_id
        self.createdBy = created_by
        self.lastEditedDateTime = last_edited_date_time
        self.page = page
        self.publishingDateTime = publishing_date_time
        self.state = state
        self.title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignCommunicationEntity"
