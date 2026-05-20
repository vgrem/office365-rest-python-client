from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPStoreAppRequestInformation(ClientValue):
    AssetId: Optional[str] = None
    BillingMarket: Optional[str] = None
    ContentMarket: Optional[str] = None
    InstallationSiteId: Optional[str] = None
    InstallationWebId: Optional[str] = None
    Justification: Optional[str] = None
    RequestType: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPStoreAppRequestInformation"
