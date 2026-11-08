from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AttributeSet(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="maxAttributesPerSet")
    @property
    def max_attributes_per_set(self) -> Optional[int]:
        """Gets the maxAttributesPerSet property"""
        return self.properties.get("maxAttributesPerSet", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttributeSet"
