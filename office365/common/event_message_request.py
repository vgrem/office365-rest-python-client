from __future__ import annotations

from typing import Optional

from office365.communications.meetings.requesttype import MeetingRequestType
from office365.entity import Entity
from office365.outlook.calendar.dateTimeTimeZone import DateTimeTimeZone
from office365.outlook.mail.location import Location
from office365.runtime.types.odata_property import odata


class EventMessageRequest(Entity):
    @odata(name="allowNewTimeProposals")
    @property
    def allow_new_time_proposals(self) -> Optional[bool]:
        """Gets the allowNewTimeProposals property"""
        return self.properties.get("allowNewTimeProposals", None)

    @odata(name="meetingRequestType")
    @property
    def meeting_request_type(self) -> MeetingRequestType:
        """Gets the meetingRequestType property"""
        return self.properties.get("meetingRequestType", MeetingRequestType.none)

    @odata(name="previousEndDateTime")
    @property
    def previous_end_date_time(self) -> DateTimeTimeZone:
        """Gets the previousEndDateTime property"""
        return self.properties.get("previousEndDateTime", DateTimeTimeZone())

    @odata(name="previousLocation")
    @property
    def previous_location(self) -> Location:
        """Gets the previousLocation property"""
        return self.properties.get("previousLocation", Location())

    @odata(name="previousStartDateTime")
    @property
    def previous_start_date_time(self) -> DateTimeTimeZone:
        """Gets the previousStartDateTime property"""
        return self.properties.get("previousStartDateTime", DateTimeTimeZone())

    @odata(name="responseRequested")
    @property
    def response_requested(self) -> Optional[bool]:
        """Gets the responseRequested property"""
        return self.properties.get("responseRequested", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EventMessageRequest"
