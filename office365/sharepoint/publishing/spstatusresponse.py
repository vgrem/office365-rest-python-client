from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.sharepointpublishingstatus import (
    SharePointPublishingStatus,
)


@dataclass
class SharePointPublishingStatusResponse(ClientValue):
    SiteId: Optional[str] = None
    Status: SharePointPublishingStatus = field(default_factory=lambda: SharePointPublishingStatus())
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePointPublishingStatusResponse"
