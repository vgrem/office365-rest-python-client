import ast
import os
from os.path import abspath

from office365.runtime.odata.type import ODataType


class TemplateContext:
    def __init__(self, template_path: str) -> None:
        self._template_path = template_path

    def build(self, schema: ODataType):
        template_file = self._resolve_template_file(schema.baseType)
        with open(template_file, encoding="utf-8") as f:
            return ast.parse(f.read())

    def _resolve_template_file(self, type_name: str):
        file_mapping = {
            "ComplexType": "complex_type.py",
            "EntityType": "entity_type.py",
        }
        path = abspath(os.path.join(self._template_path, file_mapping[type_name]))
        return path
