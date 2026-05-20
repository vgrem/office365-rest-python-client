from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class SPUninstallAddinRequest(ClientValue):
    appInstanceIds: GuidCollection = field(default_factory=GuidCollection)
    serverRelativeUrl: Optional[str] = None
    url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPUninstallAddinRequest"
