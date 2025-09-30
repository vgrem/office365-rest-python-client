from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class EmailPublishingStatus(ClientValue):

    def __init__(
        self,
        destination_url: str = None,
        error_code: int = None,
        errors: ClientValueCollection[ClientAmplifyResult] = None,
        status: int = None,
    ):
        self.DestinationURL = destination_url
        self.ErrorCode = error_code
        self.Errors = errors
        self.Status = status
