from typing import Optional

from office365.runtime.client_value import ClientValue


class SPStoreAppResponseInformation(ClientValue):
    def __init__(self, item_id: Optional[str] = None, list_id: Optional[str] = None):
        self.ItemId = item_id
        self.ListId = list_id

    ""

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPStoreAppResponseInformation"
