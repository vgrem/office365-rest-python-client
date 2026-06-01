from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class SharePointMigrationJobErrorEvent(Entity):
    @property
    def object_id(self) -> Optional[str]:
        """Gets the objectId property"""
        return self.properties.get("objectId", None)

    @property
    def object_url(self) -> Optional[str]:
        """Gets the objectUrl property"""
        return self.properties.get("objectUrl", None)

    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobErrorEvent"
