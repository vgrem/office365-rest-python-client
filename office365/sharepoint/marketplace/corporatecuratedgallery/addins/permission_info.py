from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spsitecollectionscopedpermissioninfo import (
    SPSiteCollectionScopedPermissionInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.tenantscopedpermissioninfo import (
    SPTenantScopedPermissionInfo,
)


@dataclass
class SPAddinPermissionInfo(ClientValue):
    absoluteUrl: Optional[str] = None
    allowAppOnly: Optional[bool] = None
    appIdentifier: Optional[str] = None
    serverRelativeUrl: Optional[str] = None
    siteCollectionScopedPermissions: ClientValueCollection[SPSiteCollectionScopedPermissionInfo] = field(
        default_factory=lambda: ClientValueCollection(SPSiteCollectionScopedPermissionInfo)
    )
    tenantScopedPermissions: ClientValueCollection[SPTenantScopedPermissionInfo] = field(
        default_factory=lambda: ClientValueCollection(SPTenantScopedPermissionInfo)
    )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionInfo"
