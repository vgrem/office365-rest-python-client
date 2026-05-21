from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class CampaignPublicationResetEndpointParam(ClientValue):
    EmailTranspileContent: Optional[str] = None
    EngageTranspileContent: Optional[str] = None
    ResetEndpoint: StringCollection = field(default_factory=StringCollection)
    TeamsTranspileContent: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationResetEndpointParam"
