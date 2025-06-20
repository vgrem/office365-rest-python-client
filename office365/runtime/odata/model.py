from typing import Dict

from typing_extensions import Self

from office365.runtime.odata.type import ODataType


class ODataModel:
    """Represents the type system metadata for an OData service.

    Maintains a registry of entity and complex types that make up the service's data model.
    """

    def __init__(self):
        self._types: Dict[str, ODataType] = {}

    @property
    def types(self) -> Dict[str, ODataType]:
        """Gets the type mapping dictionary.

        Returns:
            A dictionary mapping type names to their schemas
        """
        return self._types

    def add_type(self, type_schema: ODataType) -> Self:
        """Registers a type schema in the model.

        Args:
            type_schema: The type schema to register

        Returns:
            The registered type schema (for method chaining)

        Example:
            >>> model = ODataModel()
            >>> model.add_type(ODataType("User"))
        """
        self._types[type_schema.name] = type_schema
        return self

    def get_type(self, type_name: str) -> ODataType:
        """Retrieves a type schema by name.

        Args:
            type_name: The name of the type to retrieve

        Returns:
            The type schema if found

        Raises:
            KeyError: If the type is not registered
        """
        return self._types[type_name]
