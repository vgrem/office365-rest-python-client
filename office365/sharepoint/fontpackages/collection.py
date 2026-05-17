from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.fontpackages.font_package import FontPackage

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class FontPackageCollection(EntityCollection):
    """Represents a collection of View resources."""

    def __init__(self, context: ClientContext, resource_path: Optional[ResourcePath] = None) -> None:
        """Initialize a font package collection.

        Args:
            context: SharePoint client context
            resource_path: Resource path for this collection
        """
        super().__init__(context, FontPackage, resource_path)

    def get_by_title(self, title: str) -> FontPackage:
        """Gets the font package with the specified title.

        Args:
            title: The case-sensitive title of the font package to retrieve

        Returns:
            FontPackage: The font package object (not yet loaded from server)

        Raises:
            ValueError: If title is empty or None
        """
        return FontPackage(
            self.context,
            ServiceOperationPath("GetByTitle", [title], self.resource_path),
        )
