from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class SharePointMigrationJobStartEvent(Entity):
    @property
    def is_restarted(self) -> Optional[bool]:
        """Gets the isRestarted property"""
        return self.properties.get("isRestarted", None)

    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobStartEvent"
