from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class EmailPublishingStatus(ClientValue):
    def __init__(
        self,
        destination_url: Optional[str] = None,
        error_code: Optional[int] = None,
        errors: Optional[ClientValueCollection[ClientAmplifyResult]] = None,
        status: Optional[int] = None,
    ):
        self.DestinationURL = destination_url
        self.ErrorCode = error_code
        self.Errors = errors
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.EmailPublishingStatus"
