from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class AuthenticationContextClassReference(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isAvailable")
    @property
    def is_available(self) -> Optional[bool]:
        """Gets the isAvailable property"""
        return self.properties.get("isAvailable", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationContextClassReference"
