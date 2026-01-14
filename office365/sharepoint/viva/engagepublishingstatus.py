from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class VivaEngagePublishingStatus(ClientValue):
    def __init__(
        self,
        destination_id: str = None,
        error_code: int = None,
        error_message: str = None,
        errors: ClientValueCollection[ClientAmplifyResult] = ClientValueCollection(ClientAmplifyResult),
        status: int = None,
    ):
        self.DestinationId = destination_id
        self.ErrorCode = error_code
        self.ErrorMessage = error_message
        self.Errors = errors
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.VivaEngagePublishingStatus"
