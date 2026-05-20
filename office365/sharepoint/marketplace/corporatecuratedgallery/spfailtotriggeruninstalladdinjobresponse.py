from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPFailToTriggerUninstallAddinJobResponse(ClientValue):
    appInstanceId: Optional[str] = None
    errorMessage: Optional[str] = None
    serverRelativeUrl: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPFailToTriggerUninstallAddinJobResponse"
