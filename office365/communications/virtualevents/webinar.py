from __future__ import annotations

from typing import TYPE_CHECKING

from office365.communications.meetings.audience import MeetingAudience
from office365.communications.virtualevents.virtual_event import VirtualEvent
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.user_identity import CommunicationsUserIdentity
    from office365.communications.virtualevents.registration import (
        VirtualEventRegistration,
    )
    from office365.communications.virtualevents.webinar_registration_configuration import (
        VirtualEventWebinarRegistrationConfiguration,
    )


class VirtualEventWebinar(VirtualEvent):
    """Contains information about a virtual event webinar."""

    @odata(name="audience")
    @property
    def audience(self) -> MeetingAudience:
        """Gets the audience property"""
        return self.properties.get("audience", MeetingAudience.everyone)

    @odata(name="coOrganizers")
    @property
    def co_organizers(self) -> ClientValueCollection[CommunicationsUserIdentity]:
        """Gets the coOrganizers property"""
        from office365.communications.user_identity import CommunicationsUserIdentity

        return self.properties.get(
            "coOrganizers", ClientValueCollection[CommunicationsUserIdentity](CommunicationsUserIdentity)
        )

    @odata(name="registrationConfiguration", navigation=True)
    @property
    def registration_configuration(self) -> VirtualEventWebinarRegistrationConfiguration:
        """Gets the registrationConfiguration property"""
        from office365.communications.virtualevents.webinar_registration_configuration import (
            VirtualEventWebinarRegistrationConfiguration,
        )

        return self.properties.get(
            "registrationConfiguration",
            VirtualEventWebinarRegistrationConfiguration(
                self.context, ResourcePath("registrationConfiguration", self.resource_path)
            ),
        )

    @odata(name="registrations", navigation=True)
    @property
    def registrations(self) -> EntityCollection[VirtualEventRegistration]:
        """Gets the registrations property"""
        from office365.communications.virtualevents.registration import (
            VirtualEventRegistration,
        )

        return self.properties.get(
            "registrations",
            EntityCollection[VirtualEventRegistration](
                self.context, VirtualEventRegistration, ResourcePath("registrations", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventWebinar"
