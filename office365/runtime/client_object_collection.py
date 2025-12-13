from typing import Any, Callable, Dict, Generic, Iterator, List, Optional, Type, Union

from typing_extensions import Self

from office365.runtime.client_object import ClientObject, T
from office365.runtime.client_runtime_context import ClientRuntimeContext
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.event_handler import EventHandler
from office365.runtime.types.exceptions import NotFoundException


class ClientObjectCollection(ClientObject, Generic[T]):
    """
    A strongly-typed collection container for SharePoint client objects.

    This collection supports:
    - Server-driven paging for large result sets
    - LINQ-style query operations (filter, order, skip, top)
    - Type-safe object creation and manipulation
    - Event-based loading notifications
    """

    def __init__(
        self,
        context: ClientRuntimeContext,
        item_type: Type[T],
        resource_path: Optional[ResourcePath] = None,
        parent: Optional[ClientObject] = None,
    ) -> None:
        """
        Initialize a new collection of client objects.

        Args:
            context: Client context for API operations
            item_type: The class type of items in this collection
            resource_path: Relative API path for this collection
            parent: Parent object that owns this collection
        """
        super().__init__(context, resource_path)
        self._data: list[T] = []
        self._item_type: Type[T] = item_type
        self._page_loaded = EventHandler(False)
        self._paged_mode: bool = False
        self._current_pos: Optional[int] = None
        self._next_request_url: Optional[str] = None
        self._parent = parent

    def clear_state(self) -> Self:
        """
        Reset the collection's internal state while maintaining configuration.

        Note:
            In paged mode, only clears the next page pointer, preserving loaded items.

        Returns:
            self: Supports fluent method chaining
        """
        if not self._paged_mode:
            self._data = []
        self._next_request_url = None
        self._current_pos = len(self._data)
        return self

    def create_typed_object(
        self,
        initial_properties: Optional[Dict] = None,
        resource_path: Optional[ResourcePath] = None,
    ) -> T:
        """
        Factory method to create a new item of the collection's type.

        Args:
            initial_properties: Property values to initialize the object with
            resource_path: Custom API path for the new object

        Returns:
            T: New instance of the collection's item type

        Raises:
            AttributeError: If no item type was specified for the collection
        """
        if self._item_type is None:
            raise AttributeError("Cannot create object - no type specified for collection")
        if resource_path is None:
            resource_path = ResourcePath(None, self.resource_path)
        client_object = self._item_type(context=self.context, resource_path=resource_path)
        if initial_properties is not None:
            [client_object.set_property(k, v) for k, v in initial_properties.items() if v is not None]
        return client_object

    def set_property(self, key: Union[str, int], value: Dict[str, Any], persist_changes: bool = False) -> Self:
        """
        Set a property on the collection or handle special properties.

        Special Cases:
            - "__nextLinkUrl": Stores pagination URL for server-driven paging

        Args:
            key: Property name or index
            value: Property value to set
            persist_changes: Whether to mark the change for server update

        Returns:
            self: Supports fluent method chaining
        """
        if key == "__nextLinkUrl":
            self._next_request_url = value
        else:
            client_object = self.create_typed_object()
            self.add_child(client_object)
            [client_object.set_property(k, v, persist_changes) for k, v in value.items()]
        return self

    def add_child(self, client_object: T) -> Self:
        """
        Add an item to the collection and set its parent reference.

        Args:
            client_object: The item to add to the collection

        Returns:
            self: Supports fluent method chaining
        """
        client_object._parent_collection = self
        self._data.append(client_object)
        return self

    def remove_child(self, client_object: T) -> Self:
        """
        Remove an item from the collection.

        Args:
            client_object: The item to remove

        Returns:
            self: Supports fluent method chaining
        """
        self._data = [item for item in self._data if item != client_object]
        return self

    def __iter__(self) -> Iterator[T]:
        """Iterate through all items, automatically handling paged results."""
        yield from self._data

        # Handle server-side paging
        if self._paged_mode:
            while self.has_next:
                self._get_next().execute_query()
                next_items = self._data[self._current_pos :]
                yield from next_items

    def __len__(self) -> int:
        """Get the current number of loaded items in the collection."""
        return len(self._data)

    def __repr__(self) -> str:
        """Developer-friendly string representation of the collection."""
        return f"entity_type_name={self.entity_type_name}(count={len(self)})"

    def __getitem__(self, index: int) -> T:
        """Get an item by its index position."""
        return self._data[index]

    def to_json(self, json_format: Optional[ODataJsonFormat] = None) -> List[Dict[str, Any]]:
        """
        Serialize the collection to JSON format.

        Args:
            json_format: Serialization options

        Returns:
            JSON-serializable list of item dictionaries
        """
        return [item.to_json(json_format) for item in self._data]

    def filter(self, expression: str) -> Self:
        """
        Get the first item matching the filter criteria.

        Args:
            expression: OData filter expression

        Returns:
            T: The first matching item

        Raises:
            ValueError: If no matching items found
        """
        self.query_options.filter = expression
        return self

    def order_by(self, value: str) -> Self:
        """
        Add sorting to the query.

        Args:
            value: OData order expression (e.g. "CreatedDate desc")

        Returns:
            self: Supports fluent method chaining
        """
        self.query_options.order_by = value
        return self

    def skip(self, value: int) -> Self:
        """
        Skip the specified number of items in the query results.

        Args:
            value: Number of items to skip

        Returns:
            self: Supports fluent method chaining
        """
        self.query_options.skip = value
        return self

    def top(self, value: int) -> Self:
        """
        Limit the number of items returned by the query.

        Args:
            value: Maximum number of items to return

        Returns:
            self: Supports fluent method chaining
        """
        self.query_options.top = value
        return self

    def paged(self, page_size: int = None, page_loaded: Callable[[Self], None] = None) -> Self:
        """
        Enable server-driven paging mode.

        Args:
            page_size: Items per page (uses server default if None)
            page_loaded: Callback when each page loads

        Returns:
            self: Supports fluent method chaining
        """
        self._paged_mode = True
        if callable(page_loaded):
            self._page_loaded += page_loaded
        if page_size:
            self.top(page_size)
        return self

    def get(self) -> Self:
        """
        Load the collection data from the server.

        Returns:
            self: Supports fluent method chaining
        """

        def _loaded(col: Self) -> None:
            self._page_loaded(self)

        self.context.load(self).after_execute(_loaded)
        return self

    def get_all(self, page_size: int = None, page_loaded: Callable[[Self], None] = None) -> Self:
        """
        Load all items in the collection, automatically handling paging.

        Args:
            page_size: Items per page (uses server default if None)
            page_loaded: Callback when each page loads

        Returns:
            self: Supports fluent method chaining
        """

        def _page_loaded(col: Self) -> None:
            if self.has_next:
                self._get_next().after_execute(_page_loaded)

        self.paged(page_size, page_loaded).get().after_execute(_page_loaded)
        return self

    def _get_next(self) -> Self:
        """Submit a request to retrieve next collection of items"""

        def _construct_request(request: RequestOptions) -> None:
            request.url = self._next_request_url

        return self.get().before_execute(_construct_request)

    def first(self, expression: str) -> Optional[T]:
        """
        Get the first item matching the filter criteria.

        Args:
            expression: OData filter expression

        Returns:
            T: The first matching item

        Raises:
            ValueError: If no matching items found
        """
        return_type = self.create_typed_object()
        self.add_child(return_type)

        def _after_loaded(col: ClientObjectCollection) -> None:
            if len(col) < 1:
                message = f"Not found for filter: {self.query_options.filter}"
                raise ValueError(message)
            [return_type.set_property(k, v, False) for k, v in col[0].properties.items()]

        self.get().filter(expression).top(1).after_execute(_after_loaded)
        return return_type

    def single(self, expression: str) -> Optional[T]:
        """
        Get exactly one item matching the filter criteria.

        Args:
            expression: OData filter expression

        Returns:
            T: The single matching item

        Raises:
            NotFoundException: If no items match
            ValueError: If multiple items match
        """
        return_type = self.create_typed_object()
        self.add_child(return_type)

        def _after_loaded(col: ClientObjectCollection) -> None:
            if len(col) == 0:
                raise NotFoundException(return_type, expression)
            elif len(col) > 1:
                message = f"Ambiguous match found for filter: {expression}"
                raise ValueError(message)
            [return_type.set_property(k, v, False) for k, v in col[0].properties.items()]

        self.get().filter(expression).top(2).after_execute(_after_loaded)
        return return_type

    @property
    def parent(self) -> ClientObject:
        """Get the parent object that owns this collection."""
        return self._parent

    @property
    def has_next(self) -> bool:
        """Check if more pages are available in server-driven paging."""
        return self._next_request_url is not None

    @property
    def current_page(self) -> List[T]:
        """Get items from the most recently loaded page."""
        return self._data[self._current_pos :]

    @property
    def entity_type_name(self) -> str:
        """Get the OData type name for this collection."""
        if self._entity_type_name is None:
            client_object = self.create_typed_object()
            self._entity_type_name = f"Collection({client_object.entity_type_name})"
        return self._entity_type_name
