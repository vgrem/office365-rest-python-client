from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SharePointMigrationJobCancelledEvent(Entity):
    @odata(name="isCancelledByUser")
    @property
    def is_cancelled_by_user(self) -> Optional[bool]:
        """Gets the isCancelledByUser property"""
        return self.properties.get("isCancelledByUser", None)

    @odata(name="totalRetryCount")
    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobCancelledEvent"
