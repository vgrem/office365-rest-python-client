from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.communications.quotas import VIRTUAL_EVENT_QUOTAS
from office365.communications.virtualevents.presenter import VirtualEventPresenter
from office365.communications.virtualevents.session import VirtualEventSession
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.limits import limit
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.virtualevents.communications_identity_set import (
        CommunicationsIdentitySet,
    )
    from office365.communications.virtualevents.external_information import (
        VirtualEventExternalInformation,
    )
    from office365.communications.virtualevents.settings import VirtualEventSettings
    from office365.communications.virtualevents.status import VirtualEventStatus
    from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone


@limit(*VIRTUAL_EVENT_QUOTAS)
class VirtualEvent(Entity):
    """Represents an abstract base type for a virtual event.
    Base type of virtualEventTownhall and virtualEventWebinar."""

    @property
    def description(self) -> Optional[str]:
        """A description of the virtual event."""
        return self.properties.get("Description", ItemBody())

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
        from office365.communications.virtualevents.communications_identity_set import (
            CommunicationsIdentitySet,
        )

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
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("endDateTime", DateTimeTimeZone())

    @odata(name="externalEventInformation")
    @property
    def external_event_information(self) -> ClientValueCollection[VirtualEventExternalInformation]:
        """Gets the externalEventInformation property"""
        from office365.communications.virtualevents.external_information import (
            VirtualEventExternalInformation,
        )

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
        from office365.communications.virtualevents.settings import VirtualEventSettings

        return self.properties.get("settings", VirtualEventSettings())

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> DateTimeTimeZone:
        """Gets the startDateTime property"""
        from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone

        return self.properties.get("startDateTime", DateTimeTimeZone())

    @odata(name="status")
    @property
    def status(self) -> VirtualEventStatus:
        """Gets the status property"""
        from office365.communications.virtualevents.status import VirtualEventStatus

        return self.properties.get("status", VirtualEventStatus.draft)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEvent"
