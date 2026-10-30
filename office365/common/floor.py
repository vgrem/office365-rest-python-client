from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Floor(Entity):
    @odata(name="sortOrder")
    @property
    def sort_order(self) -> Optional[int]:
        """Gets the sortOrder property"""
        return self.properties.get("sortOrder", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Floor"
