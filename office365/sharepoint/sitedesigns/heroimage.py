from office365.runtime.client_value import ClientValue
from typing import Optional


class HeroImage(ClientValue):
    def __init__(self, image: Optional[str] = None):
        self.image = image

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.HeroImage"
