from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identity_set import IdentitySet


class Request(Entity):
    @odata(name="approvalId")
    @property
    def approval_id(self) -> Optional[str]:
        """Gets the approvalId property"""
        return self.properties.get("approvalId", None)

    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> Optional[datetime]:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        from office365.directory.identity_set import IdentitySet

        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="customData")
    @property
    def custom_data(self) -> Optional[str]:
        """Gets the customData property"""
        return self.properties.get("customData", None)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Request"
