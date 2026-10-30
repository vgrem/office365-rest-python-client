from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SiteCollectionAppCatalogAllowedItem(Entity):
    """An entry in the site collection app catalog allow list."""

    @odata(name="SiteID", beta=True)
    @property
    def site_id(self) -> Optional[str]:
        """The ID of a site collection in the allow list."""
        return self.properties.get("SiteID", None)

    @odata(name="AbsoluteUrl", beta=True)
    @property
    def absolute_url(self) -> Optional[str]:
        """The absolute URL of a site collection in the allow list."""
        return self.properties.get("AbsoluteUrl", None)

    @property
    def property_ref_name(self):
        return "AbsoluteUrl"

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Marketplace.CorporateCuratedGallery.SiteCollectionAppCatalogAllowedItem"

    @odata(name="ErrorMessage", beta=True)
    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)
