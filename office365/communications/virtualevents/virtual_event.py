from __future__ import annotations

from typing import Optional

from typing_extensions import Self

from office365.communications.quotas import VIRTUAL_EVENT_QUOTAS
from office365.communications.virtualevents.communications_identity_set import CommunicationsIdentitySet
from office365.communications.virtualevents.external_information import VirtualEventExternalInformation
from office365.communications.virtualevents.presenter import VirtualEventPresenter
from office365.communications.virtualevents.session import VirtualEventSession
from office365.communications.virtualevents.settings import VirtualEventSettings
from office365.communications.virtualevents.status import VirtualEventStatus
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.item_body import ItemBody
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.limits import limit
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata


@limit(*VIRTUAL_EVENT_QUOTAS)
class VirtualEvent(Entity):
    """Represents an abstract base type for a virtual event.
    Base type of virtualEventTownhall and virtualEventWebinar."""

    @odata(name="description")
    @property
    def description(self) -> ItemBody:
        """A description of the virtual event."""
        return self.properties.get("description", ItemBody())

    @odata(name="presenters", navigation=True)
    @property
    def presenters(self):
        """The virtual event presenters."""
        return self.properties.get(
            "presenters",
            EntityCollection(
                self.context,
                VirtualEventPresenter,
                ResourcePath("presenters", self.resource_path),
            ),
        )

    @odata(name="sessions", navigation=True)
    @property
    def sessions(self):
        """The virtual event presenters."""
        return self.properties.get(
            "sessions",
            EntityCollection(
                self.context,
                VirtualEventSession,
                ResourcePath("sessions", self.resource_path),
            ),
        )

    @odata(name="createdBy")
    @property
    def created_by(self) -> CommunicationsIdentitySet:
        """Gets the createdBy property"""
        return self.properties.get("createdBy", CommunicationsIdentitySet())

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> DateTimeTimeZone:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", DateTimeTimeZone())

    @odata(name="externalEventInformation")
    @property
    def external_event_information(self) -> ClientValueCollection[VirtualEventExternalInformation]:
        """Gets the externalEventInformation property"""
        return self.properties.get(
            "externalEventInformation",
            ClientValueCollection[VirtualEventExternalInformation](VirtualEventExternalInformation),
        )

    @odata(name="isRegistrationRequired")
    @property
    def is_registration_required(self) -> Optional[bool]:
        """Gets the isRegistrationRequired property"""
        return self.properties.get("isRegistrationRequired", None)

    @odata(name="settings")
    @property
    def settings(self) -> VirtualEventSettings:
        """Gets the settings property"""
        return self.properties.get("settings", VirtualEventSettings())

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> DateTimeTimeZone:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", DateTimeTimeZone())

    @odata(name="status")
    @property
    def status(self) -> VirtualEventStatus:
        """Gets the status property"""
        return self.properties.get("status", VirtualEventStatus.draft)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEvent"

    @require_permission(delegated=["VirtualEvent.ReadWrite"])
    def cancel(self) -> Self:
        """cancel operation."""
        qry = ServiceOperationQuery(self, "cancel", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(delegated=["VirtualEvent.ReadWrite"])
    def publish(self) -> Self:
        """publish operation."""
        qry = ServiceOperationQuery(self, "publish", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @require_permission(delegated=["VirtualEvent.ReadWrite"])
    def set_external_event_information(self, external_event_id: str) -> Self:
        """setExternalEventInformation operation.

        Args:
            external_event_id (str):
                externalEventId parameter
        """
        qry = ServiceOperationQuery(
            self, "setExternalEventInformation", None, {"externalEventId": external_event_id}, None, None
        )
        self.context.add_query(qry)
        return self
