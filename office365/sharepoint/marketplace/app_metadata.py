from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class CorporateCatalogAppMetadata(Entity):
    """App metadata for apps stored in the corporate catalog."""

    def __str__(self):
        return self.title or self.entity_type_name

    def deploy(self, skip_feature_deployment: bool) -> Self:
        """This method deploys an app on the app catalog.  It MUST be called in the context of the tenant app
        catalog web or it will fail.

        Args:
            skip_feature_deployment (bool): Specifies whether the app can be centrally deployed across the tenant.
        """
        payload = {"skipFeatureDeployment": skip_feature_deployment}
        qry = ServiceOperationQuery(self, "Deploy", None, payload)
        self.context.add_query(qry)
        return self

    def remove(self) -> Self:
        """This is the inverse of the add step above. One removed from the app catalog,
        the solution can't be deployed."""
        qry = ServiceOperationQuery(self, "Remove")
        self.context.add_query(qry)
        return self

    def install(self) -> Self:
        """This method allows an app which is already deployed to be installed on a web."""
        qry = ServiceOperationQuery(self, "Install")
        self.context.add_query(qry)
        return self

    def uninstall(self) -> Self:
        """This method uninstalls an app from a web."""
        qry = ServiceOperationQuery(self, "Uninstall")
        self.context.add_query(qry)
        return self

    @property
    def aad_permissions(self) -> Optional[str]:
        """ """
        return self.properties.get("AadPermissions", None)

    @property
    def app_catalog_version(self) -> Optional[str]:
        """The version of the app stored in the corporate catalog."""
        return self.properties.get("AppCatalogVersion", None)

    @property
    def can_upgrade(self) -> Optional[bool]:
        """Whether an existing instance of an app can be upgraded."""
        return self.properties.get("CanUpgrade", None)

    @property
    def is_client_side_solution(self) -> Optional[bool]:
        """Whether the app is a client-side solution."""
        return self.properties.get("IsClientSideSolution", None)

    @property
    def title(self) -> Optional[str]:
        """The title of the app."""
        return self.properties.get("Title", None)

    @property
    def id(self) -> Optional[str]:
        """The identifier of the app."""
        return self.properties.get("ID", None)

    @property
    def property_ref_name(self):
        return "ID"

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.CorporateCatalogAppMetadata"

    @property
    def aad_app_id(self) -> Optional[str]:
        """Gets the AadAppId property"""
        return self.properties.get("AadAppId", None)

    @property
    def cdn_location(self) -> Optional[str]:
        """Gets the CDNLocation property"""
        return self.properties.get("CDNLocation", None)

    @property
    def contains_tenant_wide_extension(self) -> Optional[bool]:
        """Gets the ContainsTenantWideExtension property"""
        return self.properties.get("ContainsTenantWideExtension", None)

    @property
    def current_version_deployed(self) -> Optional[bool]:
        """Gets the CurrentVersionDeployed property"""
        return self.properties.get("CurrentVersionDeployed", None)

    @property
    def deployed(self) -> Optional[bool]:
        """Gets the Deployed property"""
        return self.properties.get("Deployed", None)

    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    @property
    def id_(self) -> Optional[str]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @property
    def installed_version(self) -> Optional[str]:
        """Gets the InstalledVersion property"""
        return self.properties.get("InstalledVersion", None)

    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the IsEnabled property"""
        return self.properties.get("IsEnabled", None)

    @property
    def is_package_default_skip_feature_deployment(self) -> Optional[bool]:
        """Gets the IsPackageDefaultSkipFeatureDeployment property"""
        return self.properties.get("IsPackageDefaultSkipFeatureDeployment", None)

    @property
    def is_valid_app_package(self) -> Optional[bool]:
        """Gets the IsValidAppPackage property"""
        return self.properties.get("IsValidAppPackage", None)

    @property
    def product_id(self) -> Optional[str]:
        """Gets the ProductId property"""
        return self.properties.get("ProductId", None)

    @property
    def short_description(self) -> Optional[str]:
        """Gets the ShortDescription property"""
        return self.properties.get("ShortDescription", None)

    @property
    def skip_deployment_feature(self) -> Optional[bool]:
        """Gets the SkipDeploymentFeature property"""
        return self.properties.get("SkipDeploymentFeature", None)

    @property
    def store_asset_id(self) -> Optional[str]:
        """Gets the StoreAssetId property"""
        return self.properties.get("StoreAssetId", None)

    @property
    def supports_teams_tabs(self) -> Optional[bool]:
        """Gets the SupportsTeamsTabs property"""
        return self.properties.get("SupportsTeamsTabs", None)

    @property
    def thumbnail_url(self) -> Optional[str]:
        """Gets the ThumbnailUrl property"""
        return self.properties.get("ThumbnailUrl", None)

    def retract(self) -> Self:
        """Retract operation."""
        qry = ServiceOperationQuery(self, "Retract", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def upgrade(self) -> Self:
        """Upgrade operation."""
        qry = ServiceOperationQuery(self, "Upgrade", None, {}, None, None)
        self.context.add_query(qry)
        return self
