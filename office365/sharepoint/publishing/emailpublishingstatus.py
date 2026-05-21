from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


@dataclass
class EmailPublishingStatus(ClientValue):
    DestinationURL: Optional[str] = None
    ErrorCode: Optional[int] = None
    Errors: Optional[ClientValueCollection[ClientAmplifyResult]] = None
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.EmailPublishingStatus"
