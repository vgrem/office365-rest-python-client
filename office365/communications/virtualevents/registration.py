from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.communications.virtualevents.attendeeregistrationstatus import VirtualEventAttendeeRegistrationStatus
from office365.communications.virtualevents.external_registration_information import (  # noqa: E501
    VirtualEventExternalRegistrationInformation,
)
from office365.communications.virtualevents.registration_question_answer import VirtualEventRegistrationQuestionAnswer
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.virtualevents.session import VirtualEventSession


class VirtualEventRegistration(Entity):
    @odata(name="cancelationDateTime")
    @property
    def cancelation_date_time(self) -> Optional[datetime]:
        """Gets the cancelationDateTime property"""
        return self.properties.get("cancelationDateTime", datetime.min)

    @odata(name="email")
    @property
    def email(self) -> Optional[str]:
        """Gets the email property"""
        return self.properties.get("email", None)

    @odata(name="externalRegistrationInformation")
    @property
    def external_registration_information(self) -> VirtualEventExternalRegistrationInformation:
        """Gets the externalRegistrationInformation property"""
        return self.properties.get("externalRegistrationInformation", VirtualEventExternalRegistrationInformation())

    @odata(name="firstName")
    @property
    def first_name(self) -> Optional[str]:
        """Gets the firstName property"""
        return self.properties.get("firstName", None)

    @odata(name="lastName")
    @property
    def last_name(self) -> Optional[str]:
        """Gets the lastName property"""
        return self.properties.get("lastName", None)

    @odata(name="preferredLanguage")
    @property
    def preferred_language(self) -> Optional[str]:
        """Gets the preferredLanguage property"""
        return self.properties.get("preferredLanguage", None)

    @odata(name="preferredTimezone")
    @property
    def preferred_timezone(self) -> Optional[str]:
        """Gets the preferredTimezone property"""
        return self.properties.get("preferredTimezone", None)

    @odata(name="registrationDateTime")
    @property
    def registration_date_time(self) -> Optional[datetime]:
        """Gets the registrationDateTime property"""
        return self.properties.get("registrationDateTime", datetime.min)

    @odata(name="registrationQuestionAnswers")
    @property
    def registration_question_answers(self) -> ClientValueCollection[VirtualEventRegistrationQuestionAnswer]:
        """Gets the registrationQuestionAnswers property"""
        return self.properties.get(
            "registrationQuestionAnswers",
            ClientValueCollection[VirtualEventRegistrationQuestionAnswer](VirtualEventRegistrationQuestionAnswer),
        )

    @odata(name="status")
    @property
    def status(self) -> VirtualEventAttendeeRegistrationStatus:
        """Gets the status property"""
        return self.properties.get("status", VirtualEventAttendeeRegistrationStatus.registered)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @odata(name="sessions", navigation=True)
    @property
    def sessions(self) -> EntityCollection[VirtualEventSession]:
        """Gets the sessions property"""
        from office365.communications.virtualevents.session import VirtualEventSession

        return self.properties.get(
            "sessions",
            EntityCollection[VirtualEventSession](
                self.context, VirtualEventSession, ResourcePath("sessions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.VirtualEventRegistration"
