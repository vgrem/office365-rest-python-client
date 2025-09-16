import ast
import os
from os.path import abspath
from typing import cast

from generator.builders.property_builder import PropertyBuilder
from office365.runtime.odata.type import ODataType


class TemplateContext:
    def __init__(self, template_path: str) -> None:
        self._template_path = template_path

    def load(self, schema: ODataType):
        template_file = self._resolve_template_file(schema.baseType)
        with open(template_file, encoding="utf-8") as f:
            return ast.parse(f.read())

    def build_getter(self, builder: PropertyBuilder) -> ast.FunctionDef:
        """Build the getter property method"""
        docstring = f"Gets the {builder.schema.name} property"
        method_name = builder.name
        prop_name = builder.schema.name
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

    def _resolve_template_file(self, type_name: str):
        file_mapping = {
            "ComplexType": "complex_type.py",
            "EntityType": "entity_type.py",
        }
        path = abspath(os.path.join(self._template_path, file_mapping[type_name]))
        return path
