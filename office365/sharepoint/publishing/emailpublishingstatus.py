from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


class EmailPublishingStatus(ClientValue):
    DestinationURL: Optional[str] = None
    ErrorCode: Optional[int] = None
    Errors: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.EmailPublishingStatus"
