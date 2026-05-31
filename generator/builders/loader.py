from __future__ import annotations

import ast
import os
from os.path import abspath

from office365.runtime.odata.type_information import TypeInformation


class TemplateLoader:
    """Loads the base AST template for a given OData base type."""

    _FILE_MAP: dict[str, str] = {
        "ComplexType": "complex_type.py",
        "EntityType": "entity_type.py",
        "EnumType": "enum_type.py",
    }

    def __init__(self, template_path: str, schema: TypeInformation) -> None:
        self._template_path = template_path
        self._schema = schema

    def load(self) -> ast.Module:
        """Parse the template file and return its AST."""
        file_name = self._FILE_MAP[self._schema.BaseTypeFullName]
        path = abspath(os.path.join(self._template_path, file_name))
        with open(path, encoding="utf-8") as f:
            return ast.parse(f.read())
