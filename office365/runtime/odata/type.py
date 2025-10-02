from __future__ import annotations

import datetime
import uuid
from typing import Optional, Type, TypeVar

from typing_extensions import Self

from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.odata.member import ODataMember
from office365.runtime.odata.property import ODataProperty
from office365.runtime.types.collections import GuidCollection, StringCollection

T = TypeVar("T", bound=Type)


_PRIMITIVE_TYPES = {
    "Edm.Boolean": bool,
    "Edm.Int32": int,
    "Edm.Int64": int,
    "Edm.String": str,
    "Edm.DateTimeOffset": datetime.datetime,
    "Edm.Guid": uuid.UUID,
    "Collection(SP.KeyValue)": dict,
    "Edm.Single": float,
    "Edm.Double": float,
    "Edm.Binary": bytes,
    "Collection(Edm.Guid)": GuidCollection,
    "Collection(Edm.String)": StringCollection,
    "Collection(Edm.Int32)": ClientValueCollection[int],
    "Edm.DateTime": datetime.datetime,
}


class ODataType:
    """OData type system utilities with enhanced type resolution."""

    def __init__(
        self, class_name: str = None, namespace: str = None, base_type: str = None
    ):
        self.className = class_name
        self.namespace = namespace
        self.baseType = base_type
        self.properties = {}
        self.members = {}
        self.methods = {}

    @property
    def name(self):
        return f"{self.namespace}.{self.className}"

    @classmethod
    def register_type(cls, client_type: T, odata_type: str) -> None:
        """Registers a custom type mapping.

        Args:
            client_type: The Python type to register
            odata_type: The corresponding OData type name

        Example:
            >>> import decimal
            >>> ODataType.register_type(decimal.Decimal, "Edm.Decimal")
        """
        _PRIMITIVE_TYPES[odata_type] = client_type

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

        for odata_type, py_type in _PRIMITIVE_TYPES.items():
            if py_type == client_type:
                return odata_type
        return None

    @classmethod
    def is_primitive_type(cls, type_name: str) -> bool:
        """Checks if a type is a known OData primitive type."""
        return any(odata_type == type_name for odata_type in _PRIMITIVE_TYPES.keys())

    @classmethod
    def get_model_type(cls, type_name: str) -> Optional[Type]:
        """Returns the Model type for a given OData type name."""
        return _PRIMITIVE_TYPES.get(type_name, None)

    def add_property(self, schema: ODataProperty) -> Self:
        self.properties[schema.name] = schema
        return self

    def add_member(self, schema: ODataMember) -> Self:
        self.members[schema.name] = schema
        return self
