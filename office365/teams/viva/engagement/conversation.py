from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.teams.viva.engagement.creationmode import EngagementCreationMode


class EngagementConversation(Entity):
    @property
    def creation_mode(self) -> EngagementCreationMode:
        """Gets the creationMode property"""
        return self.properties.get("creationMode", EngagementCreationMode.none)

    @property
    def starter_id(self) -> Optional[str]:
        """Gets the starterId property"""
        return self.properties.get("starterId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EngagementConversation"
