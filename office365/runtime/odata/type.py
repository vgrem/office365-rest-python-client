from __future__ import annotations

import datetime
import importlib
import inspect
import pkgutil
import uuid
from functools import lru_cache
from typing import Optional, Sequence, Type, TypeVar

from office365.runtime.client_value_collection import ClientValueCollection
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
        self,
        class_name: str = None,
        namespace: str = None,
        base_type_name: str = "ClientValue",
        is_collection=False,
    ):
        self.className = class_name
        self.namespace = namespace
        self.baseType = base_type_name
        self.is_collection = is_collection

    @classmethod
    def resolve_client_type_name(cls, type_name: str) -> str:
        """Parse OData type and return ClientValue format string"""

        if ODataType.is_primitive_type(type_name):
            return _PRIMITIVE_TYPES.get(type_name).__name__

        is_collection = False

        if type_name.startswith("Collection(") and type_name.endswith(")"):
            is_collection = True
            type_name = type_name[len("Collection(") : -1]

        parts = type_name.split(".")
        class_name = parts[-1]

        if is_collection:
            return f"ClientValueCollection[{class_name}]"
        else:
            return class_name

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
        # return any(odata_type == type_name for odata_type in _PRIMITIVE_TYPES.keys())
        return type_name in _PRIMITIVE_TYPES

    @staticmethod
    @lru_cache(maxsize=512)
    def find_client_type(class_name: str, modules: Sequence[str]) -> Optional[Type]:
        for module_name in modules:
            try:
                module = importlib.import_module(module_name.strip())
                for _, name, _ in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
                    submodule = importlib.import_module(name)
                    if hasattr(submodule, class_name):
                        cls = getattr(submodule, class_name)
                        if inspect.isclass(cls):
                            return cls
            except (ImportError, AttributeError):
                continue
        return None
