from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class HeroImage(ClientValue):
    image: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.HeroImage"
