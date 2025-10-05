from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.statusresponse import PublishingStatusResponse


class AmplifyPublishingHistoryResult(ClientValue):

    def __init__(
        self,
        amplify_id: str = None,
        page_id: int = None,
        publication_metadata: str = None,
        publishing_status_response: PublishingStatusResponse = PublishingStatusResponse(),
        timestamp_utc: datetime = None,
    ):
        self.AmplifyId = amplify_id
        self.PageId = page_id
        self.PublicationMetadata = publication_metadata
        self.publishingStatusResponse = publishing_status_response
        self.TimestampUTC = timestamp_utc

    @property
    def entity_type_name(self):
        return "SP.Publishing.AmplifyPublishingHistoryResult"
