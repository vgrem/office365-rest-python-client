from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.search.datasourcecontainerstatus import DataSourceContainerStatus
from office365.security.search.datasourceholdstatus import DataSourceHoldStatus


class DataSourceContainer(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="holdStatus")
    @property
    def hold_status(self) -> DataSourceHoldStatus:
        """Gets the holdStatus property"""
        return self.properties.get("holdStatus", DataSourceHoldStatus.notApplied)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="releasedDateTime")
    @property
    def released_date_time(self) -> Optional[datetime]:
        """Gets the releasedDateTime property"""
        return self.properties.get("releasedDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> DataSourceContainerStatus:
        """Gets the status property"""
        return self.properties.get("status", DataSourceContainerStatus.active)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DataSourceContainer"
