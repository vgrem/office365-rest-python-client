from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.publishing.amplify.result import ClientAmplifyResult
from office365.sharepoint.publishing.emailpublishingstatus import EmailPublishingStatus as _EmailPublishingStatus
from office365.sharepoint.publishing.spstatusresponse import SharePointPublishingStatusResponse
from office365.sharepoint.teams.statusresponse import TeamsPublishingStatusResponse
from office365.sharepoint.viva.engagepublishingstatus import VivaEngagePublishingStatus as _VivaEngagePublishingStatus


@dataclass
class PublishingStatusResponse(ClientValue):
    EmailPublishingStatus: _EmailPublishingStatus = field(default_factory=lambda: _EmailPublishingStatus())
    LastTriedAt: Optional[datetime] = None
    PrePublishValidationErrorCode: Optional[int] = None
    PublishingStatus: Optional[int] = None
    SharePointPublishingStatus: ClientValueCollection[SharePointPublishingStatusResponse] = field(
        default_factory=lambda: ClientValueCollection(SharePointPublishingStatusResponse)
    )
    TeamsPublishingStatus: ClientValueCollection[TeamsPublishingStatusResponse] = field(
        default_factory=lambda: ClientValueCollection(TeamsPublishingStatusResponse)
    )
    VivaEngagePublishingStatus: _VivaEngagePublishingStatus = field(default_factory=lambda: _VivaEngagePublishingStatus())
    VivaEngageV2PublishingStatus: ClientValueCollection[_VivaEngagePublishingStatus] = field(
        default_factory=lambda: ClientValueCollection(_VivaEngagePublishingStatus)
    )
    YammerPublishingStatus: dict = field(default_factory=dict)
    Errors: ClientValueCollection[ClientAmplifyResult] = field(
        default_factory=lambda: ClientValueCollection(ClientAmplifyResult)
    )

    @property
    def entity_type_name(self):
        return "SP.Publishing.PublishingStatusResponse"
