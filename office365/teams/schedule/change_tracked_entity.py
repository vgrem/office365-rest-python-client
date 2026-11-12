from __future__ import annotations

from datetime import datetime

from typing_extensions import Self

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb


class ChangeTrackedEntity(Entity):
    """Represents an entity to track changes made to any supported schedule and associated resource."""

    @odata(name="createdDateTime", readonly=True)
    @property
    def created_datetime(self) -> datetime:
        """
        The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z
        """
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_datetime(self) -> datetime:
        """
        The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z
        """
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="lastModifiedBy", readonly=True)
    @property
    def last_modified_by(self) -> IdentitySet:
        """Identity of the person who last modified the entity."""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime", readonly=True)
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="lastModifiedDateTime", readonly=True)
    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChangeTrackedEntity"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["Schedule.ReadWrite.All", "Group.ReadWrite.All"],
        application=["Schedule.ReadWrite.All"],
    )
    def stage_for_deletion(self) -> Self:
        """stageForDeletion operation."""
        qry = ServiceOperationQuery(self, "stageForDeletion", None, {}, None, None)
        self.context.add_query(qry)
        return self
