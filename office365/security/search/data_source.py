from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.search.datasourceholdstatus import DataSourceHoldStatus


class DataSource(Entity):
    """The dataSource entity is an abstract base class used to identify sources of content for eDiscovery."""

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", IdentitySet())

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.DataSource"
