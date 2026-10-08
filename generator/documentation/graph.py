"""
Microsoft Graph documentation: injects descriptions from the OpenAPI spec.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from generator.builders.type import TypeBuilder
from generator.documentation.base import DocumentationProvider


class GraphDocumentation(DocumentationProvider):
    """Injects property and member descriptions from the Graph OpenAPI YAML.

    Descriptions become docstrings on generated types, properties and enum
    members.
    """

    def __init__(self) -> None:
        self._schemas = self._load_schemas()

    def _load_schemas(self) -> dict[str, Any]:
        """Load the ``components/schemas`` section from the OpenAPI YAML."""
        try:
            import yaml

            path = Path(__file__).parent / "graphopenapi.yaml"
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                return {}
            components = data.get("components", {})
            if not isinstance(components, dict):
                return {}
            schemas = components.get("schemas", {})
            return schemas if isinstance(schemas, dict) else {}
        except Exception:
            return {}

    def build_documentation(self, type_builder: TypeBuilder) -> None:
        """Inject descriptions from the OpenAPI spec into the type builder."""
        schema = self._schemas.get(type_builder.entity_type_name)
        if schema is None:
            return
        type_info = self._extract_type_info(schema)
        if type_info is None:
            return

        description = type_info.get("description") or schema.get("description")
        if description:
            type_builder._docstring = description

        props = type_info.get("properties", {})
        for prop in type_builder.properties:
            prop_schema = props.get(prop.schema.Name)
            if prop_schema and "description" in prop_schema:
                prop.docstring = prop_schema["description"]

    @staticmethod
    def _extract_type_info(schema: dict[str, Any]) -> dict[str, Any] | None:
        """Extract the type's properties from its schema.

        Handles both flat schemas and the ``allOf`` pattern used by Graph:
        ``allOf: [$ref parent, {title, properties}]`` — the second entry holds
        this type's own properties.
        """
        all_of = schema.get("allOf")
        if all_of and len(all_of) > 1:
            return all_of[1]
        if all_of and len(all_of) == 1:
            return all_of[0]
        if "properties" in schema:
            return schema
        return None
