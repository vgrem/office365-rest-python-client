from __future__ import annotations

import ast
import inspect
from typing import TYPE_CHECKING, ClassVar

from generator.builders.type_descriptor import ParameterType

if TYPE_CHECKING:
    from generator.builders.property import PropertyBuilder
    from generator.builders.type_resolver import ClientTypeResolver


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
        "ClientResult": "office365.runtime.client_result",
        "ServiceOperationQuery": "office365.runtime.queries.service_operation",
        "FunctionQuery": "office365.runtime.queries.function",
        "Self": "typing_extensions",
        "ClientContext": "office365.sharepoint.client_context",
        "GraphClient": "office365.graph_client",
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
        "list",
    }

    def __init__(self, resolver: "ClientTypeResolver") -> None:
        self._resolver = resolver
        self._entries: dict[str, str] = {}
        self.needs_dataclass = False

    def add(self, type_name: str) -> None:
        """Track a known type reference."""
        module = self.KNOWN.get(type_name)
        if module:
            self._entries[type_name] = module

    def add_custom(self, prop: PropertyBuilder) -> None:
        """Resolve a custom (non-builtin) type reference."""
        prop_type = prop.client_type_name
        if prop_type in self.KNOWN or prop_type in self.OPTIONAL_TYPES:
            return
        if prop.is_object_type:
            return
        cls = prop.resolve_client_type()
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

    def add_method(self, method, context_type: str = "ClientContext") -> None:
        """Track imports required by a generated operation method."""
        schema = method.schema
        if schema.IsStatic:
            self.add(context_type)
        self.add("FunctionQuery" if schema.Kind == "function" else "ServiceOperationQuery")
        if schema.ReturnTypeFullName:
            self._add_python_type(method.return_annotation)
        elif not schema.IsStatic:
            self.add("Self")
        for param in schema.Parameters or []:
            type_name = param.get("Type")
            if type_name:
                param_type = ParameterType(str(type_name))
                self._add_python_type(param_type.annotation)
                if param_type.wrapper:
                    self.add(param_type.wrapper)

    def _add_python_type(self, type_name: str) -> None:
        """Add a Python type name (resolving custom types to their modules)."""
        if "[" in type_name and type_name.endswith("]"):
            self._add_python_type(type_name.split("[", 1)[1][:-1])
        base_name = type_name.split("[")[0]
        self.add(base_name)
        if base_name in self.KNOWN or base_name in self.OPTIONAL_TYPES:
            return
        cls = self._resolver.resolve(base_name)
        if cls is not None:
            mod = inspect.getmodule(cls)
            if mod is not None:
                self._entries[base_name] = mod.__name__

    def build(self) -> list[ast.ImportFrom]:
        """Generate sorted, deduplicated import statements."""
        imports: list[ast.ImportFrom] = []

        if self.needs_dataclass:
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

        modules: dict[str, list[str]] = {}
        for type_name, module in self._entries.items():
            modules.setdefault(module, []).append(type_name)
        for module, names in sorted(modules.items()):
            imports.append(
                ast.ImportFrom(
                    module=module,
                    names=[ast.alias(name=name, asname=None) for name in sorted(names)],
                    level=0,
                )
            )

        return imports
