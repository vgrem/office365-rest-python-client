from typing import Optional
from uuid import UUID

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class SiteCollectionAppCatalogAllowedItem(Entity):
    """An entry in the site collection app catalog allow list."""

    @property
    def site_id(self) -> Optional[str]:
        """The ID of a site collection in the allow list."""
        return self.properties.get("SiteID", None)

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

    @property
    def error_message(self) -> Optional[str]:
        """Gets the ErrorMessage property"""
        return self.properties.get("ErrorMessage", None)

    def remove(self, absolute_path: str) -> Self:
        """Remove operation.

        Args:
            absolute_path (str): absolutePath parameter
        """
        qry = ServiceOperationQuery(self, "Remove", None, {"absolutePath": absolute_path}, None, None)
        self.context.add_query(qry)
        return self

    def remove_by_id(self, site_id: UUID) -> Self:
        """RemoveById operation.

        Args:
            site_id (UUID): siteId parameter
        """
        qry = ServiceOperationQuery(self, "RemoveById", None, {"siteId": site_id}, None, None)
        self.context.add_query(qry)
        return self
