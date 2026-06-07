from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class TargetedManagedAppProtection(Entity):
    @property
    def is_assigned(self) -> Optional[bool]:
        """Gets the isAssigned property"""
        return self.properties.get("isAssigned", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TargetedManagedAppProtection"
