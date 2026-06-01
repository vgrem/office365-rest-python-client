from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity


class SharePointMigrationJobPostponedEvent(Entity):
    @property
    def jobs_in_queue(self) -> Optional[int]:
        """Gets the jobsInQueue property"""
        return self.properties.get("jobsInQueue", None)

    @property
    def next_pickup_date_time(self) -> datetime:
        """Gets the nextPickupDateTime property"""
        return self.properties.get("nextPickupDateTime", datetime.min)

    @property
    def reason(self) -> Optional[str]:
        """Gets the reason property"""
        return self.properties.get("reason", None)

    @property
    def total_retry_count(self) -> Optional[int]:
        """Gets the totalRetryCount property"""
        return self.properties.get("totalRetryCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationJobPostponedEvent"
