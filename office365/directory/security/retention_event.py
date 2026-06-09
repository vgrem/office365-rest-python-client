from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.directory.security.triggertypes.event_type import RetentionEventType
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class RetentionEvent(Entity):
    @property
    def created_by(self) -> IdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", IdentitySet())

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def event_trigger_date_time(self) -> datetime:
        """Gets the eventTriggerDateTime property"""
        return self.properties.get("eventTriggerDateTime", datetime.min)

    @property
    def last_modified_by(self) -> IdentitySet:
        """Gets the lastModifiedBy property"""
        return self.properties.get("lastModifiedBy", IdentitySet())

    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @property
    def last_status_update_date_time(self) -> datetime:
        """Gets the lastStatusUpdateDateTime property"""
        return self.properties.get("lastStatusUpdateDateTime", datetime.min)

    @property
    def retention_event_type(self) -> RetentionEventType:
        """Gets the retentionEventType property"""
        return self.properties.get(
            "retentionEventType",
            RetentionEventType(self.context, ResourcePath("retentionEventType", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RetentionEvent"
