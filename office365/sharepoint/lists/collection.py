from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.sharepoint.lists.list import List

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class ListCollection(EntityCollection[List]):
    """Represents a collection of SharePoint lists."""

    def __init__(
        self,
        context: ClientContext,
        resource_path: Optional[ResourcePath] = None,
    ):
        """
        Initialize a new list collection instance.

        Args:
            context: SharePoint client context
            resource_path: Resource path for the list collection
        """
        super().__init__(context, List, resource_path)

    def get_by_title(self, list_title: str) -> List:
        """
        Get a list by its display title.

        Args:
            list_title: The display name of the list

        Returns:
            List: The requested list instance
        """
        return List(
            self.context,
            ServiceOperationPath("GetByTitle", [list_title], self.resource_path),
        )

    def get_by_id(self, list_id: str) -> List:
        """
        Get a list by its unique identifier.

        Args:
            list_id: The GUID identifier of the list

        Returns:
            List: The requested list instance
        """
        return List(
            self.context, ServiceOperationPath("GetById", [list_id], self.resource_path)
        )

    def ensure_client_rendered_site_pages_library(self) -> List:
        """
        Gets or creates the default client-rendered site pages library.

        Returns:
            List: The site pages library list
        """
        return_type = List(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(
            self, "EnsureClientRenderedSitePagesLibrary", None, None, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ensure_events_list(self) -> List:
        """
        Gets or creates the default events list for the site.

        Returns:
            List: The events list
        """
        return_type = List(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(
            self, "EnsureEventsList", None, None, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ensure_site_assets_library(self) -> List:
        """
        Gets or creates the default site assets library for images and files.

        Returns:
            List: The site assets library
        """
        return_type = List(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(
            self, "ensureSiteAssetsLibrary", None, None, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ensure_site_pages_library(self) -> List:
        """
        Gets or creates the default wiki pages library.

        Returns:
            List: The site pages library
        """
        return_type = List(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(
            self, "ensureSitePagesLibrary", None, None, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def add(self, list_creation_information: ListCreationInformation) -> List:
        """
        Creates a new list in the collection.

        Args:
            list_creation_information: List creation parameters

        Returns:
            List: The newly created list
        """
        return_type = List(self.context)
        self.add_child(return_type)
        qry = CreateEntityQuery(self, list_creation_information, return_type)
        self.context.add_query(qry)
        return return_type
