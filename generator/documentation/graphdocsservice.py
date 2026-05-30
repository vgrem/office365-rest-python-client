from __future__ import annotations

from pathlib import Path
from typing import Any

from generator.builders.type import TypeBuilder
from generator.documentation.baseservice import BaseDocumentationService


class GraphOpenService(BaseDocumentationService):
    """Microsoft Graph Documentation Service using OpenAPI specification.

    Injects property and member descriptions from the Graph OpenAPI YAML as
    docstrings on generated types, properties, and enum members.
    """

    def __init__(self):
        super().__init__()
        self._schemas = self._load_schemas()

    def _load_schemas(self) -> dict[str, Any]:
        """Load the components/schemas section from the OpenAPI YAML."""
        try:
            import yaml

            path = Path(__file__).parent / "graphopenapi.yaml"
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data.get("components", {}).get("schemas", {})
        except Exception:
            return {}

    def build_documentation(self, type_builder: TypeBuilder) -> None:
        """Inject descriptions from the OpenAPI spec into the type builder."""
        type_name = type_builder.entity_type_name
        schema = self._schemas.get(type_name)
        if schema is None:
            return

        type_info = self._extract_type_info(schema)
        if type_info is None:
            return

        # Inject type-level description
        desc = type_info.get("description") or schema.get("description")
        if desc:
            type_builder._docstring = desc

        # Inject property-level descriptions
        props = type_info.get("properties", {})
        for prop in type_builder.properties:
            prop_schema = props.get(prop.schema.Name)
            if prop_schema and "description" in prop_schema:
                prop.docstring = prop_schema["description"]

    @staticmethod
    def _extract_type_info(schema: dict[str, Any]) -> dict[str, Any] | None:
        """Extract the type's properties and descriptions from its schema.

        Handles both flat schemas and the allOf pattern used by Graph:
          allOf:
            - $ref: ...           # parent type
            - title: ...
              properties: ...     # ← this is what we need
        """
        all_of = schema.get("allOf")
        if all_of and len(all_of) > 1:
            return all_of[1]
        if all_of and len(all_of) == 1:
            return all_of[0]
        if "properties" in schema:
            return schema
        return None
