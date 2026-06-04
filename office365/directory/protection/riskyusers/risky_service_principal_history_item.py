from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class RiskyServicePrincipalHistoryItem(Entity):
    @property
    def initiated_by(self) -> Optional[str]:
        """Gets the initiatedBy property"""
        return self.properties.get("initiatedBy", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.RiskyServicePrincipalHistoryItem"
