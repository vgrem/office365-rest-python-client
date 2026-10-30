from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class ResourceOperation(Entity):
    @odata(name="actionName")
    @property
    def action_name(self) -> Optional[str]:
        """Gets the actionName property"""
        return self.properties.get("actionName", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="resourceName")
    @property
    def resource_name(self) -> Optional[str]:
        """Gets the resourceName property"""
        return self.properties.get("resourceName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ResourceOperation"
