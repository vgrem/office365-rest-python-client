from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AppUpgradeAvailability(ClientValue):
    AssetId: Optional[str] = None
    IsUpgradeAvailable: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.AppUpgradeAvailability"
