from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class HostReputation(Entity):
    @property
    def score(self) -> Optional[int]:
        """Gets the score property"""
        return self.properties.get("score", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.HostReputation"
