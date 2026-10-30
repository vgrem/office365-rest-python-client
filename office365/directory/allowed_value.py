from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AllowedValue(Entity):
    @odata(name="isActive")
    @property
    def is_active(self) -> Optional[bool]:
        """Gets the isActive property"""
        return self.properties.get("isActive", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AllowedValue"
