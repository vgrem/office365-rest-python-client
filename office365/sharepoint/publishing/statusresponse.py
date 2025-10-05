from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.emailpublishingstatus import EmailPublishingStatus
from office365.sharepoint.publishing.spstatusresponse import (
    SharePointPublishingStatusResponse,
)
from office365.sharepoint.teams.statusresponse import TeamsPublishingStatusResponse
from office365.sharepoint.viva.engagepublishingstatus import VivaEngagePublishingStatus


class PublishingStatusResponse(ClientValue):

    def __init__(
        self,
        email_publishing_status: EmailPublishingStatus = EmailPublishingStatus(),
        last_tried_at: datetime = None,
        pre_publish_validation_error_code: int = None,
        publishing_status: int = None,
        share_point_publishing_status: ClientValueCollection[
            SharePointPublishingStatusResponse
        ] = ClientValueCollection(SharePointPublishingStatusResponse),
        teams_publishing_status: ClientValueCollection[
            TeamsPublishingStatusResponse
        ] = ClientValueCollection(TeamsPublishingStatusResponse),
        viva_engage_publishing_status: VivaEngagePublishingStatus = VivaEngagePublishingStatus(),
        viva_engage_v2_publishing_status: ClientValueCollection[
            VivaEngagePublishingStatus
        ] = ClientValueCollection(VivaEngagePublishingStatus),
        yammer_publishing_status: dict = None,
    ):
        self.EmailPublishingStatus = email_publishing_status
        self.LastTriedAt = last_tried_at
        self.PrePublishValidationErrorCode = pre_publish_validation_error_code
        self.PublishingStatus = publishing_status
        self.SharePointPublishingStatus = share_point_publishing_status
        self.TeamsPublishingStatus = teams_publishing_status
        self.VivaEngagePublishingStatus = viva_engage_publishing_status
        self.VivaEngageV2PublishingStatus = viva_engage_v2_publishing_status
        self.YammerPublishingStatus = yammer_publishing_status

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishingStatusResponse"
