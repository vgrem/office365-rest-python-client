from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CardDesign(ClientValue):
    description: Optional[str] = None
    id: Optional[str] = None
    serializedProperties: Optional[str] = None
    showInToolbox: Optional[bool] = None
    title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CardDesign"
