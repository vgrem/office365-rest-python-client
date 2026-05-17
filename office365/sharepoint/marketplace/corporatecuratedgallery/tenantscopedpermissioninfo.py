from typing import Optional

from office365.runtime.client_value import ClientValue


class SPTenantScopedPermissionInfo(ClientValue):
    def __init__(
        self,
        feature: Optional[str] = None,
        id_: Optional[str] = None,
        right: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        self.feature = feature
        self.id = id_
        self.right = right
        self.scope = scope

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPTenantScopedPermissionInfo"
