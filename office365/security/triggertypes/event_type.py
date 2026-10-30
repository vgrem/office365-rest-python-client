from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class RetentionEventType(Entity):
    """Represents a single group for the same type of retention events.

    When a retention event is created, it's associated with a specific event type that in turn is associated
    with a retention label. Only content with that retention label applied will be retained for the specified
    retention period. For details, see Start retention when an event occurs."""

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastModifiedBy")
    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RetentionEventType"
