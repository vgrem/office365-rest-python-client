import uuid
from typing import List

from office365.runtime.client_value_collection import ClientValueCollection


class StringCollection(ClientValueCollection[str]):
    """A type-safe collection of string values with OData serialization support."""

    def __init__(self, initial_values: List[str] = None) -> None:
        """Initialize a string collection.

        Args:
            initial_values: Optional list of string values to initialize the collection

        Example:
            >>> coll = StringCollection(["a", "b"])
            >>> coll.add("c")
        """
        super(StringCollection, self).__init__(str, initial_values)


class GuidCollection(ClientValueCollection):
    """A collection of UUID values with proper OData serialization."""

    def __init__(self, initial_values: List[uuid] = None) -> None:
        """Initialize a GUID collection.

        Args:
            initial_values: Optional list of UUIDs or UUID strings

        Example:
            >>> coll = GuidCollection()
            >>> coll.add(uuid.uuid4())
            >>> coll.add("c9a646d3-9c61-4cb7-bfcd-ee2522c8f633")

        Note:
            String values will be automatically converted to UUID objects
        """
        super(GuidCollection, self).__init__(uuid.UUID, initial_values)
