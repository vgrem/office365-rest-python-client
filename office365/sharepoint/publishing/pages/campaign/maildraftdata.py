from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CampaignPublicationMailDraftData(ClientValue):
    DraftId: Optional[str] = None
    GroupUpn: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.CampaignPublicationMailDraftData"
