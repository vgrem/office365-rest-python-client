from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.teams.publishingstatus import TeamsPublishingStatus


class TeamsPublishingStatusResponse(ClientValue):
    def __init__(
        self,
        audience_id: Optional[str] = None,
        status: TeamsPublishingStatus = TeamsPublishingStatus(),
    ):
        self.AudienceId = audience_id
        self.Status = status

    @property
    def entity_type_name(self):
        return "SP.Publishing.TeamsPublishingStatusResponse"
