from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.amplify.amplifiedchannels import AmplifiedChannels as _AmplifiedChannels
from office365.sharepoint.sharepointids import SharePointIds as _SharePointIds


@dataclass
class PublicationMetadata(ClientValue):
    AmplifiedChannels: _AmplifiedChannels = field(default_factory=lambda: _AmplifiedChannels())
    BannerImageUrl: Optional[str] = None
    CanEdit: Optional[bool] = None
    CreationDate: Optional[datetime] = None
    Id: Optional[int] = None
    ModifiedDate: Optional[datetime] = None
    SharePointIds: _SharePointIds = field(default_factory=lambda: _SharePointIds())
    Status: Optional[str] = None
    Title: Optional[str] = None
    Url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.PublicationMetadata"
