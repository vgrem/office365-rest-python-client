from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CampaignMetadata(ClientValue):
    Color: Optional[str] = None
    Description: Optional[str] = None
    Logo: Optional[str] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.CampaignMetadata"
