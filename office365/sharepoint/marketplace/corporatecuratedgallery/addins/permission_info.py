from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.marketplace.corporatecuratedgallery.spsitecollectionscopedpermissioninfo import (
    SPSiteCollectionScopedPermissionInfo,
)
from office365.sharepoint.marketplace.corporatecuratedgallery.tenantscopedpermissioninfo import (
    SPTenantScopedPermissionInfo,
)


class SPAddinPermissionInfo(ClientValue):
    """"""

    def __init__(
        self,
        absolute_url=None,
        allow_app_only: bool = None,
        app_identifier: str = None,
        server_relative_url: str = None,
        site_collection_scoped_permissions: ClientValueCollection[
            SPSiteCollectionScopedPermissionInfo
        ] = ClientValueCollection(SPSiteCollectionScopedPermissionInfo),
        tenant_scoped_permissions: ClientValueCollection[SPTenantScopedPermissionInfo] = ClientValueCollection(
            SPTenantScopedPermissionInfo
        ),
    ):
        self.absoluteUrl = absolute_url
        self.allowAppOnly = allow_app_only
        self.appIdentifier = app_identifier
        self.serverRelativeUrl = server_relative_url
        self.siteCollectionScopedPermissions = site_collection_scoped_permissions
        self.tenantScopedPermissions = tenant_scoped_permissions

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SPAddinPermissionInfo"
