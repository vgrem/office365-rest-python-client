import uuid
from enum import Enum
from typing import Any, Dict, Generic, Iterator, List, Optional, Type, TypeVar, Union

from typing_extensions import Self

from office365.runtime.client_value import ClientValue
from office365.runtime.odata.json_format import ODataJsonFormat
from office365.runtime.odata.v3.json_light_format import JsonLightFormat
from office365.runtime.utilities import parse_enum

T = TypeVar("T")


class ClientValueCollection(ClientValue, Generic[T]):
    """A type-safe collection of ClientValue objects or primitives.

    This collection provides:
    - Type enforcement through generics
    - JSON serialization following OData standards
    - Support for both primitive and complex types
    - SharePoint-compatible metadata generation

    Example:
        >>> # Create a collection of strings
        >>> str_collection = ClientValueCollection(str, ["a", "b"])
        >>> str_collection.add("c")

        >>> # Create a collection of UUIDs
        >>> uuid_collection = ClientValueCollection(uuid.UUID)
        >>> uuid_collection.add(uuid.uuid4())

        >>> # Create a collection of complex types
        >>> class Address(ClientValue): ...
        >>> addr_collection = ClientValueCollection(Address)
        >>> addr_collection.add(Address())
    """

    def __init__(
        self,
        item_type: Type[T],
        initial_values: Optional[List[T]] = None,
    ):
        """Initialize a typed collection.

        Args:
            item_type: The type of items in this collection
            initial_values: Optional initial values (list or dict for complex types)
        """
        super(ClientValueCollection, self).__init__()
        if initial_values is None:
            initial_values = []
        self._data = initial_values  # type: list[T]
        self._item_type = item_type

    def add(self, value: T) -> Self:
        """Adds an item to the collection.

        Args:
            value: Item to add (must match collection type)

        Returns:
            Self: For method chaining

        Raises:
            TypeError: If value doesn't match collection type
        """
        if not isinstance(value, self._item_type):
            raise TypeError(f"Expected {self._item_type}, got {type(value)}")
        self._data.append(value)
        return self

    def __getitem__(self, index: int) -> T:
        """Gets an item by index.

        Args:
            index: Zero-based index

        Returns:
            The item at the specified index

        Raises:
            IndexError: If index is out of range
        """
        return self._data[index]

    def __iter__(self) -> Iterator[T]:
        """Iterates through all items in the collection.

        Yields:
            Items in the collection
        """
        return iter(self._data)

    def __len__(self) -> int:
        """Gets the number of items in the collection.

        Returns:
            int: The collection count
        """
        return len(self._data)

    def __repr__(self) -> str:
        return f"ClientValueCollection[{self._item_type.__name__}]({self._data!r})"

    def to_json(self, json_format: Optional[ODataJsonFormat] = None) -> Union[List[Any], Dict[str, Any]]:
        """Serializes the collection to OData JSON format.

        Args:
            json_format: Controls serialization behavior:
                - None: Returns simple array
                - JsonLightFormat: Returns metadata-enriched structure

        Returns:
            Union[List, Dict]: Serialized data in either:
                - Simple array format
                - JsonLight format with metadata

        Example Outputs:
            Simple: ["a", "b", "c"]
            JsonLight: {
                "results": ["a", "b", "c"],
                "__metadata": {"type": "Collection(Edm.String)"}
            }
        """
        json = [v for v in self]
        for i, v in enumerate(json):
            if isinstance(v, ClientValue):
                json[i] = v.to_json(json_format)
            elif isinstance(v, uuid.UUID):
                json[i] = str(v)
        if isinstance(json_format, JsonLightFormat) and json_format.include_control_information:
            json = {
                json_format.collection: json,
                json_format.metadata_type: {"type": self.entity_type_name},
            }
        return json

    def create_typed_value(self, initial_value: Optional[T] = None) -> T:
        """Creates a new item of the collection's type.

        Args:
            initial_value: Optional initialization value

        Returns:
            A new instance of the collection's item type

        Raises:
            ValueError: If initial_value cannot be converted to item_type
        """
        if initial_value is None:
            return uuid.uuid4() if self._item_type == uuid.UUID else self._item_type()
        elif self._item_type == uuid.UUID:
            return uuid.UUID(initial_value)
        elif issubclass(self._item_type, Enum):
            return parse_enum(self._item_type, initial_value)
        elif issubclass(self._item_type, ClientValue):
            value = self._item_type()
            [value.set_property(k, v, False) for k, v in initial_value.items()]
            return value
        else:
            return initial_value

    def set_property(self, index: int, value: Any, persist_changes: bool = False):
        """Adds an item to the collection after type conversion.

        Args:
            index: Unused (maintained for interface compatibility)
            value: Value to add (will be converted to collection type)
            persist_changes: Unused (maintained for interface compatibility)

        Returns:
            Self: For method chaining
        """
        client_value = self.create_typed_value(value)
        self.add(client_value)
        return self

    @property
    def entity_type_name(self) -> str:
        from office365.runtime.odata.type import ODataType

        """Gets the OData type name for this collection.

        Returns:
            str: The collection type name (e.g., "Collection(Edm.String)")
        """
        return f"Collection({ODataType.resolve_type(self._item_type)})"
