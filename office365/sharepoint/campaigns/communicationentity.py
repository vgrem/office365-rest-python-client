from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.sharepoint.campaigns.userinfo import CampaignUserInfo


@dataclass
class CampaignCommunicationEntity(ClientValue):
    campaignId: Optional[str] = None
    channels: StringCollection = field(default_factory=StringCollection)
    communicationId: Optional[str] = None
    createdBy: CampaignUserInfo = field(default_factory=CampaignUserInfo)
    lastEditedDateTime: Optional[datetime] = None
    page: Optional[str] = None
    publishingDateTime: Optional[datetime] = None
    state: Optional[str] = None
    title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Campaigns.CampaignCommunicationEntity"
