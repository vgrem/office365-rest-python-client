from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


@dataclass
class SharePointPublishingStatus(ClientValue):
    DestinationPageId: Optional[str] = None
    DestinationPageUniqueId: Optional[str] = None
    DestinationPageURL: Optional[str] = None
    DestinationPageVersion: Optional[str] = None
    ErrorCode: Optional[int] = None
    Errors: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.SharePointPublishingStatus"
