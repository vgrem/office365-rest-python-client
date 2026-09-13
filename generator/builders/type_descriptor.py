"""Classification and Python rendering of OData type references (codegen side)."""

from __future__ import annotations

import datetime
import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.odata.type import ODataType

from generator.builders import type_mapping

if TYPE_CHECKING:
    from generator.builders.type_resolver import ClientTypeResolver

_PRIMITIVE_DEFAULTS = {
    bool: "bool()",
    int: "int()",
    float: "float()",
    str: "str()",
    bytes: "bytes()",
    uuid.UUID: "uuid.UUID(int=0)",
    datetime.datetime: "datetime.min",
    datetime.date: "datetime.min",
    datetime.time: "datetime.min",
    datetime.timedelta: "datetime.timedelta(0)",
    dict: "{}",
}


class TypeKind(Enum):
    """Shape of an OData type reference."""

    VOID = "void"
    PRIMITIVE = "primitive"
    CLIENT_VALUE = "client_value"
    ENTITY = "entity"
    PRIMITIVE_COLLECTION = "primitive_collection"
    CLIENT_VALUE_COLLECTION = "client_value_collection"
    ENTITY_COLLECTION = "entity_collection"


class ReturnType:
    """Classifies a type name once and renders its annotation and default value."""

    def __init__(self, type_name: str | None, resolver: Optional["ClientTypeResolver"] = None) -> None:
        self._name = type_name or ""
        self._resolver = resolver
        self.kind = self._classify()

    @property
    def is_void(self) -> bool:
        return self.kind is TypeKind.VOID

    @property
    def is_stream(self) -> bool:
        return self._name == "Edm.Stream"

    @property
    def annotation(self) -> str:
        """The Python type annotation for the value (without ``ClientResult`` for voids)."""
        name = self._name
        if self.kind in (TypeKind.PRIMITIVE, TypeKind.CLIENT_VALUE):
            return f"ClientResult[{type_mapping.client_type_name(name)}]"
        if self.kind is TypeKind.ENTITY:
            return type_mapping.client_type_name(name)
        if self.kind is TypeKind.PRIMITIVE_COLLECTION:
            return f"ClientResult[{self._collection_name(name)}]"
        if self.kind is TypeKind.CLIENT_VALUE_COLLECTION:
            return f"ClientResult[ClientValueCollection[{self._item_name(name)}]]"
        return f"EntityCollection[{self._item_name(name)}]"

    def default(self, context: str) -> str:
        """The expression that constructs the return value for the given context expression."""
        name = self._name
        if self.kind is TypeKind.PRIMITIVE:
            return f"ClientResult({context}, {_primitive_default(name)})"
        if self.kind is TypeKind.CLIENT_VALUE:
            return f"ClientResult({context}, {type_mapping.client_type_name(name)}())"
        if self.kind is TypeKind.ENTITY:
            return f"{type_mapping.client_type_name(name)}({context})"
        if self.kind is TypeKind.PRIMITIVE_COLLECTION:
            return f"ClientResult({context}, {self._collection_default(name)})"
        if self.kind is TypeKind.CLIENT_VALUE_COLLECTION:
            return f"ClientResult({context}, ClientValueCollection[{self._item_name(name)}]())"
        return f"EntityCollection({context}, {self._item_name(name)})"

    def _classify(self) -> TypeKind:
        name = self._name
        if not name:
            return TypeKind.VOID
        if ODataType.is_collection_name(name):
            return self._classify_collection(name)
        if ODataType.is_primitive_name(name):
            return TypeKind.PRIMITIVE
        if self._is_client_value(name):
            return TypeKind.CLIENT_VALUE
        return TypeKind.ENTITY

    def _classify_collection(self, name: str) -> TypeKind:
        item_type = ODataType.strip_collection(name)
        if ODataType.is_primitive_name(name) or ODataType.is_primitive_name(item_type):
            return TypeKind.PRIMITIVE_COLLECTION
        if self._is_client_value(item_type):
            return TypeKind.CLIENT_VALUE_COLLECTION
        return TypeKind.ENTITY_COLLECTION

    def _is_client_value(self, type_name: str | None) -> bool:
        if self._resolver is None:
            return False
        cls = self._resolver.resolve(type_name)
        return cls is not None and issubclass(cls, ClientValue)

    @staticmethod
    def _item_name(type_name: str) -> str:
        return type_mapping.client_type_name(ODataType.strip_collection(type_name))

    @staticmethod
    def _collection_name(type_name: str) -> str:
        """Python annotation for a collection whose item type is primitive."""
        mapped = ODataType.primitive_type_for(type_name) if ODataType.is_primitive_name(type_name) else None
        if mapped is None:
            return type_mapping.client_type_name(type_name)
        item_types = getattr(mapped, "__args__", None)
        if item_types:
            return f"{mapped.__name__}[{item_types[0].__name__}]"
        return mapped.__name__

    @staticmethod
    def _collection_default(type_name: str) -> str:
        """Python default expression for a collection whose item type is primitive."""
        if ODataType.is_primitive_name(type_name):
            mapped = ODataType.primitive_type_for(type_name)
            assert mapped is not None
            item_types = getattr(mapped, "__args__", None)
            if item_types:
                return f"ClientValueCollection({item_types[0].__name__})"
            return f"{mapped.__name__}()"
        item_type = ODataType.strip_collection(type_name)
        primitive = ODataType.primitive_type_for(item_type)
        if primitive is not None:
            return f"ClientValueCollection({primitive.__name__})"
        return f"{type_mapping.client_type_name(type_name)}()"


def _primitive_default(type_name: str | None) -> str:
    """Default expression for a primitive OData type (e.g. ``Edm.Int32`` -> ``int()``)."""
    return _PRIMITIVE_DEFAULTS.get(ODataType.primitive_type_for(type_name), "None")
