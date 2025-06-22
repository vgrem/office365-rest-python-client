from typing import TYPE_CHECKING, Union

from office365.entity_collection import EntityCollection
from office365.onedrive.lists.list import List
from office365.onedrive.lists.template_type import ListTemplateType
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.create_entity import CreateEntityQuery

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class ListCollection(EntityCollection[List]):
    """Represents a collection of SharePoint/OneDrive lists with enhanced query capabilities.

    Provides methods to:
    - Create new lists
    - Retrieve lists by name or ID
    - Manage list templates

    Example:
        >>> ctx = GraphClient()
        >>> lists = ListCollection(ctx)
        >>> new_list = lists.add("Project Tasks",
        ...     ListTemplateType.tasks).execute_query()
    """

    def __init__(self, context: "GraphClient", resource_path: ResourcePath = None):
        super().__init__(context, List, resource_path)

    def add(
        self,
        display_name: str,
        list_template: Union[ListTemplateType, str] = ListTemplateType.genericList,
    ) -> List:
        """Create a new list with the specified properties.

        Args:
            display_name: The displayable title of the list
            list_template: The base list template (default: generic list)

        Returns:
            List: The new list object (not yet executed)
        """
        return_type = List(self.context, EntityPath(None, self.resource_path))
        self.add_child(return_type)
        payload = {
            "displayName": display_name,
            "list": {"template": str(list_template)},
        }
        qry = CreateEntityQuery(self, payload, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_name(self, name: str) -> List:
        """Retrieve a list by its name.

        Args:
            name: The name of the list to retrieve

        Returns:
            List: The requested list object (not yet executed)
        """
        return List(self.context, EntityPath(name, self.resource_path))

    def get_by_id(self, list_id: str) -> List:
        """Retrieve a list by its ID.

        Args:
            list_id: The ID of the list to retrieve

        Returns:
            List: The requested list object (not yet executed)
        """
        return List(self.context, EntityPath(list_id, self.resource_path))
