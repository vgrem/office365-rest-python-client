from typing import Optional

from office365.runtime.client_value import ClientValue


class CampaignMetadata(ClientValue):
    def __init__(
        self,
        color: Optional[str] = None,
        description: Optional[str] = None,
        logo: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.Color = color
        self.Description = description
        self.Logo = logo
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.CampaignMetadata"
