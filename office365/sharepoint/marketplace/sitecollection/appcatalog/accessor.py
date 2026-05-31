from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.marketplace.app_metadata_collection import CorporateCatalogAppMetadataCollection


class SiteCollectionCorporateCatalogAccessor(Entity):
    """Accessor for the site collection corporate catalog."""

    @odata(name="AvailableApps")
    @property
    def available_apps(self) -> CorporateCatalogAppMetadataCollection:
        """Returns the apps available in this corporate catalog."""
        return self.properties.get(
            "AvailableApps",
            CorporateCatalogAppMetadataCollection(self.context, ResourcePath("AvailableApps", self.resource_path)),
        )

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SiteCollectionCorporateCatalogAccessor"
