from __future__ import annotations

import ast
import os
from os.path import abspath
from typing import TYPE_CHECKING, Set, cast

from office365.runtime.odata.type_information import TypeInformation

from generator.builders.member_builder import MemberBuilder
from generator.builders.property_builder import PropertyBuilder

if TYPE_CHECKING:
    from generator.builders.type_builder import TypeBuilder


class TemplateContext:
    """Template context"""

    TYPE_DEPENDENCIES = {
        "UUID": "uuid",
        "datetime": "datetime",
        "date": "datetime",
        "StringCollection": "office365.runtime.types.collections",
        "GuidCollection": "office365.runtime.types.collections",
        "Optional": "typing",
    }

    OPTIONAL_TYPES = {"str", "int", "bool", "float", "UUID", "bytes"}

    def __init__(self, template_path: str, schema: TypeInformation) -> None:
        self._template_path = template_path
        self._schema = schema
        self._required_imports: Set[str] = set()

    def load(self) -> ast.Module:
        file_mapping = {
            "ComplexType": "complex_type.py",
            "EntityType": "entity_type.py",
            "EnumType": "enum_type.py",
        }
        template_file = abspath(os.path.join(self._template_path, file_mapping[self._schema.BaseTypeFullName]))
        with open(template_file, encoding="utf-8") as f:
            return ast.parse(f.read())

    def build_imports(self, builder: TypeBuilder):
        """Add import statements for dependent types."""
        imports = []
        added_modules = set()

        for prop in builder.properties:
            prop_type = prop.client_type_name

            # Track basic type dependencies
            if prop_type in self.TYPE_DEPENDENCIES:
                self._ensure_type_dependency(prop_type)

            # Track Optional dependency if needed
            if prop_type in self.OPTIONAL_TYPES:
                self._ensure_type_dependency("Optional")

        # Build import statements
        for type_name in self._required_imports:
            module = self.TYPE_DEPENDENCIES[type_name]
            if module not in added_modules:
                imports.append(
                    ast.ImportFrom(
                        module=module,
                        names=[ast.alias(name=type_name, asname=None)],
                        level=0,
                    )
                )
                added_modules.add(module)

        return imports

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
        if prop_type_name in self.OPTIONAL_TYPES:
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

        property_code = f'''
@property
def {method_name}(self) -> {type_annotation}:
    """{docstring}"""
    return self.properties.get("{prop_name}", {default_value})
'''

        parsed = ast.parse(property_code.strip())
        return cast(ast.FunctionDef, parsed.body[0])

    def build_type_name_property(self):
        """Ensure the class has an entity_type_name property that returns the correct type name"""
        node = ast.FunctionDef(
            name="entity_type_name",
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self")],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[],
            ),
            body=[ast.Return(value=ast.Constant(value=self._schema.FullName))],
            decorator_list=[ast.Name(id="property", ctx=ast.Load())],
            returns=None,
        )

        return node

    def _ensure_type_dependency(self, type_name: str) -> None:
        """Track that a type dependency is needed"""
        if type_name in self.TYPE_DEPENDENCIES:
            self._required_imports.add(type_name)
