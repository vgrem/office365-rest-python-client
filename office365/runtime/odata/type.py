from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, Optional, Type, TypeVar

from typing_extensions import Self

from office365.runtime.odata.property import ODataProperty

# if TYPE_CHECKING:
from office365.runtime.types.collections import GuidCollection, StringCollection

T = TypeVar("T", bound=Type)


"""Primitive OData data type mapping"""
_PRIMITIVE_TYPES = {
    bool: "Edm.Boolean",
    int: "Edm.Int32",
    str: "Edm.String",
    datetime.datetime: "Edm.DateTimeOffset",
    uuid.UUID: "Edm.Guid",
    dict: "Collection(SP.KeyValue)",
    float: "Edm.Single",
    bytes: "Edm.Binary",
    GuidCollection: "Collection(Edm.Guid)",
    StringCollection: "Collection(Edm.String)",
}


class ODataType:
    """OData type system utilities with enhanced type resolution."""

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
        _PRIMITIVE_TYPES[python_type] = odata_type

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

        return _PRIMITIVE_TYPES.get(client_type, None)

    @classmethod
    def is_primitive_type(cls, client_type: T) -> bool:
        """Checks if a type is a known OData primitive type."""
        return client_type in _PRIMITIVE_TYPES

    @classmethod
    def get_model_type(cls, type_name: str) -> Optional[Type]:
        """Returns the Model type for a given OData type name."""
        for model_type, odata_name in _PRIMITIVE_TYPES.items():
            if odata_name == type_name:
                return model_type
        return None

    def add_property(self, schema: ODataProperty) -> Self:
        self.properties[schema.name] = schema
        return self
