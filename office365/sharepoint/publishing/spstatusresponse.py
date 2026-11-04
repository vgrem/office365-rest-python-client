from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.publishing.sharepointpublishingstatus import (
    SharePointPublishingStatus,
)


@value
class SharePointPublishingStatusResponse(ClientValue):
    SiteId: Optional[str] = None
    Status: SharePointPublishingStatus = field(default_factory=SharePointPublishingStatus)
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePointPublishingStatusResponse"
