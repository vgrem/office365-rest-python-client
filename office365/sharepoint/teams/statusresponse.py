from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.teams.publishingstatus import TeamsPublishingStatus


@dataclass
class TeamsPublishingStatusResponse(ClientValue):
    AudienceId: Optional[str] = None
    Status: TeamsPublishingStatus = field(default_factory=TeamsPublishingStatus)

    @property
    def entity_type_name(self):
        return "SP.Publishing.TeamsPublishingStatusResponse"
