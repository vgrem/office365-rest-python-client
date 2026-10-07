from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Optional, Type, cast

from typing_extensions import Self

from office365.runtime.client_object import ClientObjectT
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v3.entity import EntityPath
from office365.runtime.record_collection import RecordCollection
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext


class EntityCollection(RecordCollection[ClientObjectT]):
    """A type-safe collection of SharePoint entities.

    Provides strongly-typed access to SharePoint entity collections with support for:
    - Type-safe object creation
    - Fluent API patterns
    - Parent-child relationships
    """

    def __init__(
        self,
        context: ClientContext,
        item_type: Type[ClientObjectT],
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
    ) -> ClientObjectT:
        if resource_path is None:
            resource_path = EntityPath(None, self.resource_path)
        return super().create_typed_object(initial_properties, resource_path)

    def update_all(
        self,
        *,
        where: Optional[Callable[[ClientObjectT], bool]] = None,
        **properties: Any,
    ) -> Self:
        """Set properties on the matching loaded entities, queuing one update each.

        Deferred: nothing is sent until the caller executes the query. Load the
        collection first (``get()`` / ``get_all()``), then run the queued updates
        with ``execute_query()`` or — for many entities — ``execute_batch(...)``
        so they are sent as a handful of ``$batch`` requests:

            items = lst.items.get().execute_query()
            items.update_all(Status="Archived").execute_batch(concurrency=5)

        Only the entities already loaded are touched; use ``get_all()`` first to
        include every page of a paged collection.

        Args:
            where: Optional client-side predicate; only the entities it accepts
                are updated. Omit to update every loaded entity.
            **properties: The OData property names and values to set. A value may
                be a callable taking the entity, for a value derived from its
                current state::

                    items.update_all(Title=lambda i: f"{i.properties['Title']} (archived)")

        Returns:
            self: Supports method chaining.
        """
        for item in self._select(where):
            for name, value in properties.items():
                item.set_property(name, value(item) if callable(value) else value)
            item.update()
        return self

    def delete_all(
        self,
        *,
        where: Optional[Callable[[ClientObjectT], bool]] = None,
        ignore_missing: bool = False,
    ) -> Self:
        """Delete the matching loaded entities, queuing one delete each.

        Deferred: nothing is sent until the caller executes the query. Load the
        collection first (``get()`` / ``get_all()``), then run the queued deletes
        with ``execute_batch(...)`` so they are sent as a handful of ``$batch``
        requests:

            items = lst.items.get().execute_query()
            items.delete_all(where=lambda i: i.properties["Status"] == "stale") \\
                .execute_batch(concurrency=5)

        Only the entities already loaded are deleted; use ``get_all()`` first to
        include every page of a paged collection.

        Args:
            where: Optional client-side predicate; only the entities it accepts
                are deleted. Omit to delete every loaded entity.
            ignore_missing: When ``True``, deleting an entity that no longer
                exists (HTTP 404) succeeds instead of raising — making cleanup
                re-runs idempotent.

        Returns:
            self: Supports method chaining.
        """
        for item in self._select(where):
            item.delete_object(ignore_missing=ignore_missing)
        return self

    def _select(self, where: Optional[Callable[[ClientObjectT], bool]]) -> List[ClientObjectT]:
        """Snapshot the loaded entities accepted by ``where``.

        A list snapshot is required because queuing a write may detach the entity
        (a delete removes it) while the collection is being enumerated.
        """
        items = list(self._data)
        if where is None:
            return items
        return [item for item in items if where(item)]

    @property
    def context(self) -> ClientContext:
        """Gets the SharePoint client context for this collection."""
        return cast("ClientContext", self._context)
