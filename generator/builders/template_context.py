from __future__ import annotations

import ast
import inspect
import os
from enum import Enum
from os.path import abspath
from typing import Optional, cast

from office365.runtime.odata.type_information import TypeInformation

from generator.builders.collector import TypeReferenceCollector
from generator.builders.member import MemberBuilder
from generator.builders.property import PropertyBuilder


class TemplateContext:
    """Template context — orchestrates template loading and property building."""

    _FILE_MAP: dict[str, str] = {
        "ComplexType": "complex_type.py",
        "EntityType": "entity_type.py",
        "EnumType": "enum_type.py",
    }

    def __init__(self, template_path: str, schema: TypeInformation, modules: Optional[tuple[str, ...]] = None) -> None:
        self._template_path = template_path
        self._schema = schema
        self._modules = modules or ()

    def load(self) -> ast.Module:
        file_name = self._FILE_MAP[self._schema.BaseTypeFullName]
        path = abspath(os.path.join(self._template_path, file_name))
        with open(path, encoding="utf-8") as f:
            return ast.parse(f.read())

    def build_references(self, collector: TypeReferenceCollector) -> list[ast.ImportFrom]:
        """Generate import statements from a TypeReferenceCollector."""
        return collector.build()

    def build_member(self, builder: MemberBuilder):
        return ast.Assign(
            targets=[ast.Name(id=builder.name, ctx=ast.Store())],
            value=ast.Constant(value=builder.value),
        )

    def get_existing_members(self, class_node: ast.ClassDef) -> set:
        """Get set of existing member names in the class"""
        existing_members = set()

        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        existing_members.add(target.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                existing_members.add(node.target.id)

        return existing_members

    def build_get_property(self, builder: PropertyBuilder) -> ast.FunctionDef:
        """Build the getter property method"""
        docstring = f"Gets the {builder.schema.Name} property"
        method_name = builder.name
        prop_name = builder.schema.Name
        prop_type_name = builder.client_type_name
        if prop_type_name in TypeReferenceCollector.OPTIONAL_TYPES:
            type_annotation = f"Optional[{prop_type_name}]"
        else:
            type_annotation = prop_type_name
        default_value = "None"
        if builder.is_object_type:
            if builder.is_collection_type:
                default_value = (
                    f"{prop_type_name}("
                    f"self.context, "
                    f"{builder.client_item_type_name}, "
                    f"ResourcePath('{prop_name}', self.resource_path)"
                    f")"
                )
            else:
                default_value = f"{prop_type_name}(self.context, ResourcePath('{prop_name}', self.resource_path))"
        elif builder.is_collection_type:
            default_value = f"{prop_type_name}({builder.client_item_type_name})"
        elif self._modules:
            resolved = builder._client_type.resolve_client_type(self._modules)
            if resolved is not None and inspect.isclass(resolved):
                if issubclass(resolved, Enum):
                    members = list(resolved)
                    if members:
                        default_value = f"{prop_type_name}.{members[0].name}"
                elif not builder._client_type.is_primitive_type:
                    default_value = f"{prop_type_name}()"

        property_code = f'''
@property
def {method_name}(self) -> {type_annotation}:
    """{docstring}"""
    return self.properties.get("{prop_name}", {default_value})
'''

        parsed = ast.parse(property_code.strip())
        return cast(ast.FunctionDef, parsed.body[0])
