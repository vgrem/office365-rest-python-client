from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CampaignAssociation(ClientValue):
    CampaignId: Optional[int] = None
    PublicationId: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.Campaigns.Models.CampaignAssociation"
