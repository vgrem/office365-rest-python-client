from __future__ import annotations

from typing import Optional

from office365.onedrive.sharepoint.migration.event import SharePointMigrationEvent
from office365.runtime.types.odata_property import odata


class SharePointMigrationJobStartEvent(SharePointMigrationEvent):
    @odata(name="isRestarted")
    @property
    def is_restarted(self) -> Optional[bool]:
        """Gets the isRestarted property"""
        return self.properties.get("isRestarted", None)

    @odata(name="totalRetryCount")
    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobStartEvent"
