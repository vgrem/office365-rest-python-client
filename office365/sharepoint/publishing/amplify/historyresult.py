from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.statusresponse import PublishingStatusResponse


@dataclass
class AmplifyPublishingHistoryResult(ClientValue):
    AmplifyId: Optional[str] = None
    PageId: Optional[int] = None
    PublicationMetadata: Optional[str] = None
    publishingStatusResponse: PublishingStatusResponse = field(default_factory=lambda: PublishingStatusResponse())
    TimestampUTC: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyPublishingHistoryResult"
