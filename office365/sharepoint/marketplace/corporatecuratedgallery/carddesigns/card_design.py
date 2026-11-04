from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CardDesign(ClientValue):
    description: Optional[str] = None
    id: Optional[str] = None
    serializedProperties: Optional[str] = None
    showInToolbox: Optional[bool] = None
    title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CardDesign"
