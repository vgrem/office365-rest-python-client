from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class SharePointPublishingStatus(ClientValue):
    def __init__(
        self,
        destination_page_id: Optional[str] = None,
        destination_page_unique_id: Optional[str] = None,
        destination_page_url: Optional[str] = None,
        destination_page_version: Optional[str] = None,
        error_code: Optional[int] = None,
        errors: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(ClientAmplifyResult),
        status: Optional[int] = None,
    ):
        self.DestinationPageId = destination_page_id
        self.DestinationPageUniqueId = destination_page_unique_id
        self.DestinationPageURL = destination_page_url
        self.DestinationPageVersion = destination_page_version
        self.ErrorCode = error_code
        self.Errors = errors
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePointPublishingStatus"
