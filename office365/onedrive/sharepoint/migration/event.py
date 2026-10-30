from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SharePointMigrationEvent(Entity):
    @odata(name="correlationId")
    @property
    def correlation_id(self) -> Optional[str]:
        """Gets the correlationId property"""
        return self.properties.get("correlationId", None)

    @odata(name="eventDateTime")
    @property
    def event_date_time(self) -> datetime:
        """Gets the eventDateTime property"""
        return self.properties.get("eventDateTime", datetime.min)

    @odata(name="jobId")
    @property
    def job_id(self) -> Optional[str]:
        """Gets the jobId property"""
        return self.properties.get("jobId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SharePointMigrationEvent"
