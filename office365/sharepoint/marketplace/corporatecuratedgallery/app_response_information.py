from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SPStoreAppResponseInformation(ClientValue):
    ItemId: Optional[str] = None
    ListId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPStoreAppResponseInformation"
