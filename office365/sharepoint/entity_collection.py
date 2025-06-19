from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, cast

from office365.runtime.client_object import T
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v3.entity import EntityPath
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class EntityCollection(ClientObjectCollection[T]):
    """A type-safe collection of SharePoint entities.

    Provides strongly-typed access to SharePoint entity collections with support for:
    - Type-safe object creation
    - Fluent API patterns
    - Parent-child relationships

    Example:
        >>> ctx = ClientContext()
        >>> from office365.sharepoint.lists.list import List
        >>> lists = EntityCollection(ctx, List)
    """

    def __init__(
        self,
        context: ClientContext,
        item_type: Type[T],
        resource_path: Optional[ResourcePath] = None,
        parent: Optional[Entity] = None,
    ) -> None:
        """Initialize an entity collection.

        Args:
            context: SharePoint client context
            item_type: The class type of items in this collection
            resource_path: Relative resource path
            parent: Parent entity of this collection
        """
        super().__init__(context, item_type, resource_path, parent)

    def create_typed_object(
        self,
        initial_properties: Optional[dict] = None,
        resource_path: Optional[ResourcePath] = None,
    ) -> T:
        if resource_path is None:
            resource_path = EntityPath(None, self.resource_path)
        return super().create_typed_object(initial_properties, resource_path)

    @property
    def context(self) -> ClientContext:
        """Gets the SharePoint client context for this collection."""
        return cast("ClientContext", self._context)
