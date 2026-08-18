from datetime import datetime
from typing import Optional

from office365.communications.calls.transcript import CallTranscript
from office365.communications.onlinemeetings.base import OnlineMeetingBase
from office365.communications.onlinemeetings.broadcast_settings import BroadcastMeetingSettings
from office365.communications.onlinemeetings.participants import MeetingParticipants
from office365.communications.onlinemeetings.recordings.call import CallRecording
from office365.entity_collection import EntityCollection
from office365.outlook.mail.item_body import ItemBody
from office365.runtime.client_result import ClientResult
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class OnlineMeeting(OnlineMeetingBase):
    """
    Contains information about a meeting, including the URL used to join a meeting,
    the attendees list, and the description.
    """

    def get_virtual_appointment_join_web_url(self) -> ClientResult[str]:
        """Get a join web URL for a Microsoft Virtual Appointment. This web URL includes enhanced
        business-to-customer experiences such as mobile browser join and virtual lobby rooms.
        With Teams Premium, you can configure a custom lobby room experience for attendees by adding your company
        logo and access the Virtual Appointments usage report for organizational analytics.
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "getVirtualAppointmentJoinWebUrl", None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def allow_attendee_to_enable_camera(self) -> Optional[bool]:
        """Indicates whether attendees can turn on their camera."""
        return self.properties.get("allowAttendeeToEnableCamera", None)

    @property
    def allow_attendee_to_enable_mic(self) -> Optional[bool]:
        """Indicates whether attendees can turn on their microphone."""
        return self.properties.get("allowAttendeeToEnableMic", None)

    @odata(name="allowedPresenters")
    @property
    def allowed_presenters(self):
        """Specifies who can be a presenter in a meeting. Possible values are listed in the following table."""
        return self.properties.get("allowedPresenters", StringCollection())

    @property
    def allow_participants_to_change_name(self) -> Optional[bool]:
        """Specifies if participants are allowed to rename themselves in an instance of the meeting."""
        return self.properties.get("allowParticipantsToChangeName", None)

    @property
    def attendee_report(self) -> Optional[bytes]:
        """The content stream of the attendee report of a Microsoft Teams live event."""
        return self.properties.get("attendeeReport", None)

    @odata(name="broadcastSettings")
    @property
    def broadcast_settings(self) -> BroadcastMeetingSettings:
        """Settings related to a live event."""
        return self.properties.get("broadcastSettings", BroadcastMeetingSettings())

    @property
    def participants(self) -> MeetingParticipants:
        """
        The participants associated with the online meeting. This includes the organizer and the attendees.
        """
        return self.properties.get("participants", MeetingParticipants())

    @property
    def subject(self) -> Optional[str]:
        """The subject of the online meeting."""
        return self.properties.get("subject", None)

    @subject.setter
    def subject(self, value: str) -> None:
        self.set_property("subject", value)

    @odata(name="startDateTime")
    @property
    def start_datetime(self):
        """Gets the meeting start time in UTC."""
        return self.properties.get("startDateTime", datetime.min)

    @start_datetime.setter
    def start_datetime(self, value: datetime):
        self.set_property("startDateTime", value)

    @odata(name="endDateTime")
    @property
    def end_datetime(self):
        """Gets the meeting end time in UTC."""
        return self.properties.get("endDateTime", datetime.min)

    @end_datetime.setter
    def end_datetime(self, value: datetime):
        self.set_property("endDateTime", value)

    @odata(name="joinInformation")
    @property
    def join_information(self) -> ItemBody:
        """The join URL of the online meeting. Read-only."""
        return self.properties.get("joinInformation", ItemBody())

    @property
    def join_web_url(self) -> Optional[str]:
        """The join URL of the online meeting. Read-only."""
        return self.properties.get("joinWebUrl", None)

    @property
    def video_teleconference_id(self) -> Optional[str]:
        """The video teleconferencing ID."""
        return self.properties.get("videoTeleconferenceId", None)

    @property
    def recordings(self) -> EntityCollection[CallRecording]:
        """The recordings of an online meeting"""
        return self.properties.get(
            "recordings", EntityCollection(self.context, CallRecording, ResourcePath("recordings", self.resource_path))
        )

    @property
    def creation_date_time(self) -> Optional[datetime]:
        """Gets the creationDateTime property"""
        return self.properties.get("creationDateTime", datetime.min)

    @property
    def end_date_time(self) -> Optional[datetime]:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @property
    def external_id(self) -> Optional[str]:
        """Gets the externalId property"""
        return self.properties.get("externalId", None)

    @property
    def is_broadcast(self) -> Optional[bool]:
        """Gets the isBroadcast property"""
        return self.properties.get("isBroadcast", None)

    @property
    def meeting_template_id(self) -> Optional[str]:
        """Gets the meetingTemplateId property"""
        return self.properties.get("meetingTemplateId", None)

    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @property
    def transcripts(self) -> EntityCollection[CallTranscript]:
        """Gets the transcripts property"""
        return self.properties.get(
            "transcripts",
            EntityCollection[CallTranscript](
                self.context, CallTranscript, ResourcePath("transcripts", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnlineMeeting"
