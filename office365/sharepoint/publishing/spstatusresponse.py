from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.sharepointpublishingstatus import (
    SharePointPublishingStatus,
)


class SharePointPublishingStatusResponse(ClientValue):
    def __init__(
        self,
        site_id: str = None,
        status: SharePointPublishingStatus = SharePointPublishingStatus(),
        web_id: str = None,
    ):
        self.SiteId = site_id
        self.Status = status
        self.WebId = web_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePointPublishingStatusResponse"
