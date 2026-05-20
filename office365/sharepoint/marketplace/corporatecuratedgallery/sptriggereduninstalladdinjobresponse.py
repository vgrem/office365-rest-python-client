from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPTriggeredUninstallAddinJobResponse(ClientValue):
    absoluteUrl: Optional[str] = None
    appInstanceId: Optional[str] = None
    serverRelativeUrl: Optional[str] = None
    uninstallJobId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPTriggeredUninstallAddinJobResponse"
