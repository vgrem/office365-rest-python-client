from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPUninstallAddinErrorDetail(ClientValue):
    correlationId: Optional[str] = None
    detail: Optional[str] = None
    exceptionMessage: Optional[str] = None
    source: Optional[str] = None
    type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinErrorDetail"
