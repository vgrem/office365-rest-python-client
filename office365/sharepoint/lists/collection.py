from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.sharepoint.lists.list import List
from office365.sharepoint.lists.template_type import ListTemplateType

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
            self,
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
            self.context,
            ServiceOperationPath("GetById", [list_id], self.resource_path),
            self,
        )

    def ensure_client_rendered_site_pages_library(self) -> List:
        """
        Gets or creates the default client-rendered site pages library.

        Returns:
            List: The site pages library list
        """
        return_type = List(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(self, "EnsureClientRenderedSitePagesLibrary", None, None, None, return_type)
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
        qry = ServiceOperationQuery(self, "EnsureEventsList", None, None, None, return_type)
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
        qry = ServiceOperationQuery(self, "ensureSiteAssetsLibrary", None, None, None, return_type)
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
        qry = ServiceOperationQuery(self, "ensureSitePagesLibrary", None, None, None, return_type)
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

    def add_list(
        self,
        title: str,
        description: str = None,
        template_type: ListTemplateType = ListTemplateType.GenericList,
        allow_content_types: bool = False,
    ) -> List:
        """
        Creates a new list.

        :param str title: Specifies the display name of the new list.
        :param int template_type: Specifies the list server template of the new list.
        :param str or None description: Specifies the description of the new list.
        :param bool allow_content_types:
        """
        return self.add(ListCreationInformation(title, description, template_type, allow_content_types))

    def add_library(
        self,
        title: str,
        description: str = None,
        allow_content_types: bool = False,
    ) -> List:
        """Creates a document library

        Returns:
            List: The documents library
        """
        return self.add(
            ListCreationInformation(
                title,
                description,
                ListTemplateType.DocumentLibrary,
                allow_content_types,
            )
        )

    def add_tasks(
        self,
        title: str,
        description: str = None,
        allow_content_types: bool = False,
        with_timeline_and_hierarchy: bool = False,
    ) -> List:
        """Creates a Tasks list

        Returns:
            List: The Tasks list
        """
        return self.add(
            ListCreationInformation(
                title,
                description,
                (
                    ListTemplateType.TasksWithTimelineAndHierarchy
                    if with_timeline_and_hierarchy
                    else ListTemplateType.Tasks
                ),
                allow_content_types,
            )
        )
