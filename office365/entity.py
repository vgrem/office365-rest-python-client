from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from typing_extensions import Self

from office365.runtime.client_object import ClientObject, PropertyT
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.queries.delete_entity import DeleteEntityQuery
from office365.runtime.queries.update_entity import UpdateEntityQuery

if TYPE_CHECKING:
    from office365.graph_client import GraphClient


class Entity(ClientObject):
    """Base entity for Microsoft Graph objects with common CRUD operations."""

    def update(self) -> Self:
        """Updates the entity in Microsoft Graph.

        Returns:
            Self: The entity instance for method chaining

        Example:
            >>> client = GraphClient()
            >>> user = client.me
            >>> user.update().execute_query()
        """
        qry = UpdateEntityQuery(self)
        self.context.add_query(qry)
        return self

    def delete_object(self) -> Self:
        """Deletes the entity from Microsoft Graph.

        Returns:
            Self: The entity instance for method chaining

        Example:
            >>> client = GraphClient()
            >>> user = client.me
            >>> user.delete_object().execute_query()
        """
        qry = DeleteEntityQuery(self)
        self.context.add_query(qry)
        self.remove_from_parent_collection()
        return self

    @property
    def context(self) -> GraphClient:
        """Gets the GraphClient context for this entity.

        Returns:
            GraphClient: The parent client context
        """
        return cast("GraphClient", self._context)

    @property
    def entity_type_name(self) -> str:
        """Gets the Microsoft Graph type name for this entity.

        Returns:
            str: The fully qualified type name (e.g. "microsoft.graph.user")
        """
        if self._entity_type_name is None:
            name = type(self).__name__
            self._entity_type_name = "microsoft.graph." + name[0].lower() + name[1:]
        return self._entity_type_name

    @property
    def id(self) -> Optional[str]:
        """Gets the unique identifier of the entity.

        Returns:
            Optional[str]: The entity ID if available, else None
        """
        return self.properties.get("id", None)

    @property
    def property_ref_name(self) -> str:
        """Gets the name of the key property used for entity reference.

        Returns:
            str: The property name used as entity key (default: "id")
        """
        return "id"

    def set_property(
        self, name: str, value: PropertyT, persist_changes: bool = True
    ) -> Self:
        """Sets a property value and updates the resource path if needed.

        Args:
            name: The property name to set
            value: The property value
            persist_changes: Whether to persist changes immediately

        Returns:
            Self: The entity instance for method chaining
        """
        super().set_property(name, value, persist_changes)
        if name == self.property_ref_name:
            if self._resource_path is None:
                if isinstance(self.parent_collection.resource_path, EntityPath):
                    self._resource_path = self.parent_collection.resource_path.patch(
                        value
                    )
                else:
                    self._resource_path = ResourcePath(
                        value, self.parent_collection.resource_path
                    )
            else:
                self._resource_path.patch(value)
        return self
