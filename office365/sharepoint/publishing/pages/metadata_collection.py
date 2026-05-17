from typing import TypeVar

from office365.runtime.client_object import ClientObject
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity_collection import EntityCollection

ClientObjectT = TypeVar("ClientObjectT", bound=ClientObject)


class SitePageMetadataCollection(EntityCollection[ClientObjectT]):  # type: ignore[type-arg]
    """Specifies a collection of site pages."""

    def get_by_id(self, site_page_id: int) -> ClientObjectT:
        """Gets the site page with the specified ID.
        :param int site_page_id: Specifies the identifier of the site page.
        """
        from office365.sharepoint.publishing.pages.metadata import SitePageMetadata

        return SitePageMetadata(  # type: ignore[return-value]
            self.context,
            ServiceOperationPath("GetById", [site_page_id], self.resource_path),
        )
