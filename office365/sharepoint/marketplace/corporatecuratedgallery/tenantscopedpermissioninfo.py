from office365.runtime.client_value import ClientValue


class SPTenantScopedPermissionInfo(ClientValue):

    def __init__(
        self,
        feature: str = None,
        id_: str = None,
        right: str = None,
        scope: str = None,
    ):
        self.feature = feature
        self.id = id_
        self.right = right
        self.scope = scope

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPTenantScopedPermissionInfo"
