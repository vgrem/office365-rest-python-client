from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult


@dataclass
class VivaEngagePublishingStatus(ClientValue):
    DestinationId: Optional[str] = None
    ErrorCode: Optional[int] = None
    ErrorMessage: Optional[str] = None
    Errors: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )
    Status: Optional[int] = None
    CrossPostScenario: int | None = None
    DestinationType: int | None = None
    RawThreadId: str | None = None
    ThreadId: str | None = None
    ThreadStarterId: str | None = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.VivaEngagePublishingStatus"
