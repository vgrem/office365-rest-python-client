from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CampaignPublicationLoadMailDraftParam(ClientValue):
    IsPreview: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationLoadMailDraftParam"
