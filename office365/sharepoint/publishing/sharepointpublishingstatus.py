from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class SharePointPublishingStatus(ClientValue):

    def __init__(
        self,
        destination_page_id: str = None,
        destination_page_unique_id: str = None,
        destination_page_url: str = None,
        destination_page_version: str = None,
        error_code: int = None,
        errors: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(
            ClientAmplifyResult
        ),
        status: int = None,
    ):
        self.DestinationPageId = destination_page_id
        self.DestinationPageUniqueId = destination_page_unique_id
        self.DestinationPageURL = destination_page_url
        self.DestinationPageVersion = destination_page_version
        self.ErrorCode = error_code
        self.Errors = errors
        self.Status = status
