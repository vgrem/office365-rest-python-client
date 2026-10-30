from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.delegatedadmin.access_container import DelegatedAdminAccessContainer
from office365.directory.delegatedadmin.access_details import DelegatedAdminAccessDetails
from office365.directory.delegatedadmin.accessassignmentstatus import DelegatedAdminAccessAssignmentStatus
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class DelegatedAdminAccessAssignment(Entity):
    @odata(name="accessContainer")
    @property
    def access_container(self) -> DelegatedAdminAccessContainer:
        """Gets the accessContainer property"""
        return self.properties.get("accessContainer", DelegatedAdminAccessContainer())

    @odata(name="accessDetails")
    @property
    def access_details(self) -> DelegatedAdminAccessDetails:
        """Gets the accessDetails property"""
        return self.properties.get("accessDetails", DelegatedAdminAccessDetails())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="status")
    @property
    def status(self) -> DelegatedAdminAccessAssignmentStatus:
        """Gets the status property"""
        return self.properties.get("status", DelegatedAdminAccessAssignmentStatus.pending)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DelegatedAdminAccessAssignment"
