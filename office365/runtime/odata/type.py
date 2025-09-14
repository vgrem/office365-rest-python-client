from __future__ import annotations

import datetime
import uuid
from typing import Optional, Type, TypeVar

from typing_extensions import Self

from office365.runtime.odata.property import ODataProperty

T = TypeVar("T", bound=Type)


class ODataType:
    """OData type system utilities with enhanced type resolution."""

    primitive_types = {
        bool: "Edm.Boolean",
        int: "Edm.Int32",
        str: "Edm.String",
        datetime.datetime: "Edm.DateTimeOffset",
        uuid.UUID: "Edm.Guid",
        dict: "Collection(SP.KeyValue)"
    }
    """Primitive OData data type mapping"""

    def __init__(self):
        self.className = None
        self.namespace = None
        self.baseType = None
        self.properties = {}
        self.methods = {}

    @property
    def name(self):
        return f"{self.namespace}.{self.className}"

    @classmethod
    def register_type(cls, python_type: T, odata_type: str) -> None:
        """Registers a custom type mapping.

        Args:
            python_type: The Python type to register
            odata_type: The corresponding OData type name

        Example:
            >>> import decimal
            >>> ODataType.register_type(decimal.Decimal, "Edm.Decimal")
        """
        cls.primitive_types[python_type] = odata_type

    @classmethod
    def resolve_type(cls, client_type: T) -> Optional[str]:
        """Resolves the OData type name for a given Python type.

        Args:
            client_type: The Python type to resolve (class or instance)

        Returns:
            The OData type name or None if unknown

        Examples:
            >>> ODataType.resolve_type(str)
            'Edm.String'
            >>> ODataType.resolve_type(ClientValue)
            'SP.ClientValue'
        """
        from office365.runtime.client_value import ClientValue

        try:
            if issubclass(client_type, ClientValue):
                return client_type().entity_type_name
        except TypeError:
            pass

        return cls.primitive_types.get(client_type, None)

    @classmethod
    def is_primitive_type(cls, client_type: T) -> bool:
        """Checks if a type is a known OData primitive type."""
        return client_type in cls.primitive_types

    def add_property(self, prop_schema: ODataProperty) -> Self:
        name = prop_schema.normalized_name
        self.properties[name] = prop_schema
        return self
