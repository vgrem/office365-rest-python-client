from office365.runtime.client_value import ClientValue


class CampaignMetadata(ClientValue):
    def __init__(
        self,
        color: str = None,
        description: str = None,
        logo: str = None,
        title: str = None,
    ):
        self.Color = color
        self.Description = description
        self.Logo = logo
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.CampaignMetadata"
