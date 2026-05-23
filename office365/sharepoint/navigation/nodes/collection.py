from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.navigation.nodes.creationinformation import (
    NavigationNodeCreationInformation,
)
from office365.sharepoint.navigation.nodes.node import NavigationNode

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class NavigationNodeCollection(EntityCollection[NavigationNode]):
    """Represents a collection of NavigationNode resources."""

    def __init__(self, context: ClientContext, resource_path=None):
        super().__init__(context, NavigationNode, resource_path)

    def add(self, create_node_info: NavigationNodeCreationInformation) -> NavigationNode:
        """
        Creates a navigation node object and adds it to the collection.
        """
        return_type = NavigationNode(self.context)
        return_type.title = create_node_info.Title  # type: ignore[assignment]
        return_type.url = create_node_info.Url  # type: ignore[assignment]
        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    def move_after(self, node_id: int, previous_node_id: int) -> Self:
        """
        Moves a navigation node after a specified navigation node in the navigation node collection.

        Args:
            node_id: Identifier of the navigation node that is moved.
            previous_node_id: Identifier of the navigation node after which the node identified by nodeId moves to
        """
        params = {"nodeId": node_id, "previousNodeId": previous_node_id}
        qry = ServiceOperationQuery(self, "MoveAfter", params)
        self.context.add_query(qry)
        return self

    def get_by_index(self, index: int) -> NavigationNode:
        """
        Returns the navigation node at the specified index.

        Args:
            index: The index of the navigation node to be returned.
        """
        return_type = NavigationNode(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(self, "GetByIndex", [index], None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_id(self, node_id: int) -> NavigationNode:
        """Returns the navigation node with the specified identifier.
        It MUST return NULL if no navigation node corresponds to the specified identifier.

        Args:
            node_id: Specifies the identifier of the navigation node.
        """
        return NavigationNode(self.context, ServiceOperationPath("GetById", [node_id], self.resource_path))
