from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class Schema(Entity):
    @property
    def base_type(self) -> Optional[str]:
        """Gets the baseType property"""
        return self.properties.get("baseType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.Schema"
