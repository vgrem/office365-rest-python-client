from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.statusresponse import PublishingStatusResponse


class AmplifyPublishingHistoryResult(ClientValue):
    def __init__(
        self,
        amplify_id: Optional[str] = None,
        page_id: Optional[int] = None,
        publication_metadata: Optional[str] = None,
        publishing_status_response: PublishingStatusResponse = PublishingStatusResponse(),
        timestamp_utc: Optional[datetime] = None,
    ):
        self.AmplifyId = amplify_id
        self.PageId = page_id
        self.PublicationMetadata = publication_metadata
        self.publishingStatusResponse = publishing_status_response
        self.TimestampUTC = timestamp_utc

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyPublishingHistoryResult"
