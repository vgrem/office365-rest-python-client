import ast
import os
from os.path import abspath
from typing import cast

from generator.builders.member_builder import MemberBuilder
from generator.builders.property_builder import PropertyBuilder
from office365.runtime.odata.type_information import TypeInformation


class TemplateContext:
    def __init__(self, template_path: str, schema: TypeInformation) -> None:
        self._template_path = template_path
        self._schema = schema

    def load(self) -> ast.Module:
        template_file = self._resolve_template_file()
        with open(template_file, encoding="utf-8") as f:
            return ast.parse(f.read())

    def build_member(self, builder: MemberBuilder):
        return ast.Assign(
            targets=[ast.Name(id=builder.name, ctx=ast.Store())],
            value=ast.Constant(value=builder.value),
        )

    def build_getter(self, builder: PropertyBuilder) -> ast.FunctionDef:
        """Build the getter property method"""
        docstring = f"Gets the {builder.schema.Name} property"
        method_name = builder.name
        prop_name = builder.schema.Name
        prop_type_name = builder.type_name
        type_annotation = f"Optional[{prop_type_name}]"

        property_code = f'''
@property
def {method_name}(self) -> {type_annotation}:
    """{docstring}"""
    return self.properties.get("{prop_name}", None)
'''

        parsed = ast.parse(property_code.strip())
        return cast(ast.FunctionDef, parsed.body[0])

    def build_entity_type_name(self):
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

    def _resolve_template_file(self):
        file_mapping = {
            "ComplexType": "complex_type.py",
            "EntityType": "entity_type.py",
            "EnumType": "enum_type.py",
        }
        path = abspath(
            os.path.join(
                self._template_path, file_mapping[self._schema.BaseTypeFullName]
            )
        )
        return path
