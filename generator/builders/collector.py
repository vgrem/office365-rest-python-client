from __future__ import annotations

import ast
import inspect
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from generator.builders.property import PropertyBuilder


class TypeReferenceCollector:
    """Collects Python type references required by a generated OData type.

    For each property on the type, resolves the OData type name to the
    corresponding Python module path so the generator can emit the correct
    ``import`` statements.
    """

    KNOWN: ClassVar[dict[str, str]] = {
        "UUID": "uuid",
        "datetime": "datetime",
        "date": "datetime",
        "time": "datetime",
        "StringCollection": "office365.runtime.types.collections",
        "GuidCollection": "office365.runtime.types.collections",
        "Optional": "typing",
        "ResourcePath": "office365.runtime.paths.resource_path",
        "EntityCollection": "office365.entity_collection",
        "ClientValueCollection": "office365.runtime.client_value_collection",
    }

    OPTIONAL_TYPES: ClassVar[set[str]] = {
        "str",
        "int",
        "bool",
        "float",
        "UUID",
        "bytes",
        "date",
        "time",
        "dict",
        "datetime",
    }

    def __init__(self, modules: tuple[str, ...]) -> None:
        self._modules = modules
        self._entries: dict[str, str] = {}
        self._needs_dataclass = False

    def add(self, type_name: str) -> None:
        """Track a known type reference."""
        module = self.KNOWN.get(type_name)
        if module:
            self._entries[type_name] = module
        if type_name not in self.OPTIONAL_TYPES:
            self._needs_dataclass = True

    def add_custom(self, prop: PropertyBuilder) -> None:
        """Resolve a custom (non-builtin) type reference."""
        prop_type = prop.client_type_name
        if prop_type in self.KNOWN or prop_type in self.OPTIONAL_TYPES:
            return
        if prop.is_object_type:
            self._needs_dataclass = True
            return
        cls = prop._client_type.resolve_client_type(self._modules)
        if cls is not None:
            mod = inspect.getmodule(cls)
            if mod is not None:
                self._entries[prop_type] = mod.__name__

    def add_object_type(self, prop: PropertyBuilder) -> None:
        """Track type references for navigation properties."""
        self._entries["ResourcePath"] = self.KNOWN["ResourcePath"]
        prop_type = prop.client_type_name
        if prop.is_collection_type:
            if "ClientValueCollection" in prop_type or "ClientValue" in prop_type:
                self._entries["ClientValueCollection"] = self.KNOWN["ClientValueCollection"]
            else:
                self._entries["EntityCollection"] = self.KNOWN["EntityCollection"]

    def build(self) -> list[ast.ImportFrom]:
        """Generate sorted, deduplicated import statements."""
        imports: list[ast.ImportFrom] = []
        added: set[str] = set()

        if self._needs_dataclass and "dataclasses" not in added:
            imports.append(
                ast.ImportFrom(
                    module="dataclasses",
                    names=[
                        ast.alias(name="dataclass", asname=None),
                        ast.alias(name="field", asname=None),
                    ],
                    level=0,
                )
            )
            added.add("dataclasses")

        for type_name, module in sorted(self._entries.items(), key=lambda x: x[1]):
            if module not in added:
                imports.append(
                    ast.ImportFrom(
                        module=module,
                        names=[ast.alias(name=type_name, asname=None)],
                        level=0,
                    )
                )
                added.add(module)

        return imports
