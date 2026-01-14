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
    "Edm.Guid": uuid.UUID,
    "Edm.Single": float,
    "Edm.Double": float,
    "Edm.Binary": bytes,
    "Edm.DateTimeOffset": datetime.datetime,
    "Edm.DateTime": datetime.datetime,
    "Edm.Duration": datetime.timedelta,
    "Collection(SP.KeyValue)": dict,
    "Collection(Edm.Guid)": GuidCollection,
    "Collection(Edm.String)": StringCollection,
    "Collection(Edm.Int32)": ClientValueCollection[int],
}


class ODataType:
    """OData type system utilities with enhanced type resolution."""

    def __init__(self, name: str = None, is_object_type=False):
        self._name = name
        self._client_type = None
        self._is_object_type = is_object_type
        self._used_modules = None
        self._item_client_type = None

    def __repr__(self):
        return f"ODataType(name={self._name!r}, client_type={self.client_type_name!r})"

    def __str__(self):
        return self.client_type_name

    @property
    def client_type_name(self) -> str:
        """Returns the model type name representation."""
        if self._client_type:
            return self._client_type.__name__

        if self._name in _PRIMITIVE_TYPES:
            primitive_type = _PRIMITIVE_TYPES[self._name]
            return primitive_type.__name__
        elif self.is_collection:
            item_type_name = self._name[len("Collection(") : -1]
            self._item_client_type = ODataType(name=item_type_name, is_object_type=self._is_object_type)
            item_client_name = self._item_client_type.client_type_name
            if self._is_object_type:
                return f"EntityCollection[{item_client_name}]"
            else:
                return f"ClientValueCollection[{item_client_name}]"
        else:
            return self._name.split(".")[-1]

    @property
    def item_client_type(self) -> Optional[ODataType]:
        """Returns the ODataType for collection items, if this is a collection."""
        return self._item_client_type

    @property
    def client_type(self) -> Optional[Type]:
        """Returns the resolved Python type, or None if not resolved yet."""
        return self._client_type

    def resolve_client_type(self, modules: Sequence[str]) -> Optional[Type]:
        """Resolves and caches the actual Python type."""
        if self._client_type:
            return self._client_type

        modules_key = tuple(sorted(modules))
        resolved = self._resolve_type(modules_key)

        self._client_type = resolved
        self._used_modules = modules_key
        return resolved

    @lru_cache(maxsize=512)  # noqa: B019
    def _resolve_type(self, modules_key: tuple) -> Optional[Type]:
        """Internal cached resolution."""
        target_name = self.client_type_name

        def _search_module(module_name: str) -> Optional[Type]:
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, target_name):
                    cls = getattr(module, target_name)
                    if inspect.isclass(cls):
                        return cls

                if hasattr(module, "__path__"):
                    for _, name, _ in pkgutil.iter_modules(module.__path__):
                        full_name = module_name + "." + name
                        found_class = _search_module(full_name)
                        if found_class:
                            return found_class

            except (ImportError, AttributeError):
                pass
            return None

        for m_name in modules_key:
            result = _search_module(m_name.strip())
            if result:
                return result
        return None

    @classmethod
    def resolve_type_name(cls, client_type: T) -> Optional[str]:
        """Resolves the OData type name for a given Python type.

        Args:
            client_type: The Python type to resolve (class or instance)

        Returns:
            The OData type name or None if unknown

        Examples:
            >>> ODataType.resolve_type_name(str)
            'Edm.String'
            >>> ODataType.resolve_type_name(ClientValue)
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

    @property
    def is_primitive_type(self) -> bool:
        """Checks if a type is a known OData primitive type."""
        return self._name in _PRIMITIVE_TYPES

    @property
    def is_collection(self) -> bool:
        """Check if this type represents a collection."""
        return self._name.startswith("Collection(")
