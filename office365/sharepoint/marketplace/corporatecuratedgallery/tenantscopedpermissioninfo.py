from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPTenantScopedPermissionInfo(ClientValue):
    feature: Optional[str] = None
    id: Optional[str] = None
    right: Optional[str] = None
    scope: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPTenantScopedPermissionInfo"
