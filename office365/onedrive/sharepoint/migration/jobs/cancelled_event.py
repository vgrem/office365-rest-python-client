from __future__ import annotations

from typing import Optional

from office365.entity import Entity


class SharePointMigrationJobCancelledEvent(Entity):
    @property
    def is_cancelled_by_user(self) -> Optional[bool]:
        """Gets the isCancelledByUser property"""
        return self.properties.get("isCancelledByUser", None)

    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobCancelledEvent"
