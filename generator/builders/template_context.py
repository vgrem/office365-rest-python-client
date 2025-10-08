import ast
import os
from os.path import abspath
from typing import cast

from generator.builders.member_builder import MemberBuilder
from generator.builders.property_builder import PropertyBuilder
from generator.builders.type_builder import TypeBuilder
from office365.runtime.odata.type_information import TypeInformation


class TemplateContext:
    """Template context"""

    def __init__(self, template_path: str, schema: TypeInformation) -> None:
        self._template_path = template_path
        self._schema = schema

    def load(self) -> ast.Module:
        file_mapping = {
            "ComplexType": "complex_type.py",
            "EntityType": "entity_type.py",
            "EnumType": "enum_type.py",
        }
        template_file = abspath(
            os.path.join(
                self._template_path, file_mapping[self._schema.BaseTypeFullName]
            )
        )
        with open(template_file, encoding="utf-8") as f:
            return ast.parse(f.read())

    def build_imports(self, builder: TypeBuilder):
        """Add import statements for dependent types."""
        imports = []
        for prop in builder.properties:
            pass
        return imports

    def build_member(self, builder: MemberBuilder):
        return ast.Assign(
            targets=[ast.Name(id=builder.name, ctx=ast.Store())],
            value=ast.Constant(value=builder.value),
        )

    def build_get_property(self, builder: PropertyBuilder) -> ast.FunctionDef:
        """Build the getter property method"""
        docstring = f"Gets the {builder.schema.Name} property"
        method_name = builder.name
        prop_name = builder.schema.Name
        prop_type_name = builder.client_type_name
        type_annotation = f"Optional[{prop_type_name}]"

        property_code = f'''
@property
def {method_name}(self) -> {type_annotation}:
    """{docstring}"""
    return self.properties.get("{prop_name}", None)
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
