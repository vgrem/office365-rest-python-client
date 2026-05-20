from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


@dataclass
class TeamsPublishingStatus(ClientValue):
    AudienceId: Optional[str] = None
    ErrorCode: Optional[int] = None
    ErrorMessage: Optional[str] = None
    Errors: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )
    HttpStatusCode: Optional[int] = None
    Status: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TeamsPublishingStatus"
