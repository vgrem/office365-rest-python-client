from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class AuthenticationContextClassReference(Entity):
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def is_available(self) -> Optional[bool]:
        """Gets the isAvailable property"""
        return self.properties.get("isAvailable", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AuthenticationContextClassReference"
