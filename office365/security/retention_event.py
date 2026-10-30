from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.security.triggertypes.event_type import RetentionEventType

if TYPE_CHECKING:
    from office365.security.event_propagation_result import (
        EventPropagationResult,
    )
    from office365.security.event_query import EventQuery
    from office365.security.retention_event_status import RetentionEventStatus


class RetentionEvent(Entity):
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

    @odata(name="eventTriggerDateTime")
    @property
    def event_trigger_date_time(self) -> datetime:
        """Gets the eventTriggerDateTime property"""
        return self.properties.get("eventTriggerDateTime", datetime.min)

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

    @odata(name="lastStatusUpdateDateTime")
    @property
    def last_status_update_date_time(self) -> datetime:
        """Gets the lastStatusUpdateDateTime property"""
        return self.properties.get("lastStatusUpdateDateTime", datetime.min)

    @odata(name="retentionEventType", navigation=True)
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

    @odata(name="eventPropagationResults")
    @property
    def event_propagation_results(self) -> ClientValueCollection[EventPropagationResult]:
        """Gets the eventPropagationResults property"""
        from office365.security.event_propagation_result import (
            EventPropagationResult,
        )

        return self.properties.get(
            "eventPropagationResults", ClientValueCollection[EventPropagationResult](EventPropagationResult)
        )

    @odata(name="eventQueries")
    @property
    def event_queries(self) -> ClientValueCollection[EventQuery]:
        """Gets the eventQueries property"""
        from office365.security.event_query import EventQuery

        return self.properties.get("eventQueries", ClientValueCollection[EventQuery](EventQuery))

    @odata(name="eventStatus")
    @property
    def event_status(self) -> RetentionEventStatus:
        """Gets the eventStatus property"""
        from office365.security.retention_event_status import (
            RetentionEventStatus,
        )

        return self.properties.get("eventStatus", RetentionEventStatus())
