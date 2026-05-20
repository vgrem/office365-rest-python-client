from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPStoreAppCreateByIdInformation(ClientValue):
    CallerId: Optional[str] = None
    CMU: Optional[str] = None
    isUpdatingApp: Optional[bool] = None
    Overwrite: Optional[bool] = None
    SkipFeatureDeployment: Optional[bool] = None
    StoreAssetId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPStoreAppCreateByIdInformation"
