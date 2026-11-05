from typing import Optional

from office365.runtime.client_value import ClientValue


class StoreAppCreationInformation(ClientValue):
    IconUrl: Optional[str] = None
    Publisher: Optional[str] = None
    ShortDescription: Optional[str] = None
    StoreAssetId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.StoreAppCreationInformation"
