from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class TeamsPublishingStatus(ClientValue):

    def __init__(
        self,
        audience_id: str = None,
        error_code: int = None,
        error_message: str = None,
        errors: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(
            ClientAmplifyResult
        ),
        http_status_code: int = None,
        status: int = None,
    ):
        self.AudienceId = audience_id
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.Errors = errors
        self.HttpStatusCode = http_status_code
        self.Status = status
