from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List

from typing_extensions import Self

from office365.communications.onlinemeetings.online_meeting import OnlineMeeting
from office365.communications.onlinemeetings.participants import MeetingParticipants
from office365.communications.onlinemeetings.recordings.call import CallRecording
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_value import ClientValue
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.runtime.operations import ProgressCallback


class ChatInfo(ClientValue):
    messageId: str | None = None

    replyChainMessageId: str | None = None

    threadId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatInfo"


class OnlineMeetingCollection(EntityCollection[OnlineMeeting]):
    """
    A meeting's ``externalId`` is its idempotency key, so every import into this
    collection books with ``createOrGet`` rather than a plain create: a replayed
    file returns the meetings it already booked. A record must therefore carry
    ``externalId`` (plus ``subject``/``startDateTime``/``endDateTime``); use
    :meth:`create` for an ad-hoc meeting that has no key of yours.
    """

    def __init__(self, context, resource_path=None):
        super().__init__(context, OnlineMeeting, resource_path)

    def create(
        self,
        subject: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        **kwargs,
    ) -> OnlineMeeting:
        """Create an online meeting on behalf of a user by using the object ID (OID) in the user token.

        Args:
            start_datetime (datetime): The meeting start time in UTC.
            end_datetime (datetime): The meeting end time in UTC.
            subject (str): The subject of the online meeting.
        """
        return super().add(subject=subject, startDateTime=start_datetime, endDateTime=end_datetime, **kwargs)

    @verb(role="action", effect="write")
    @require_permission(delegated=["OnlineMeetings.ReadWrite"], application=["OnlineMeetings.ReadWrite.All"])
    def create_or_get(
        self,
        external_id: str | None = None,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        subject: str | None = None,
        participants: MeetingParticipants | None = None,
        chat_info: ChatInfo | None = None,
        **kwargs,
    ) -> OnlineMeeting:
        """Create an onlineMeeting object with a custom specified external ID. If the external ID already exists,
        this API will return the onlineMeeting object with that external ID.

        Args:
            external_id (str): The external ID. A custom ID. (Required)
            start_datetime (datetime.datetime): The meeting start time in UTC.
            end_datetime (datetime.datetime): The meeting end time in UTC.
            subject (str): The subject of the online meeting.
            participants (MeetingParticipants): The participants associated with the online meeting.
              This includes the organizer and the attendees.
            chat_info (ChatInfo):
        """
        return_type = OnlineMeeting(self.context)
        self.add_child(return_type)
        payload = {
            "externalId": external_id,
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
            "subject": subject,
            "chatInfo": chat_info,
            "participants": participants,
        }
        payload.update({name: value for name, value in kwargs.items() if value is not None})
        qry = ServiceOperationQuery(self, "createOrGet", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def _import_records(self, records: List[dict], progress: ProgressCallback | None = None) -> Self:
        """Queue one ``createOrGet`` per record, so importing a file twice books nothing twice.

        The record keys are the meeting's own — ``externalId``, ``subject``,
        ``startDateTime``, ``endDateTime`` — which is what an import maps a file
        header onto, so a CSV with those columns needs no per-row code.
        """
        from office365.runtime.operations import query_progress_hook

        hook = query_progress_hook(len(records), progress) if callable(progress) else None
        for record in records:
            self.create_or_get(**record)
            if hook is not None:
                self.context.after_execute(hook)
        return self

    @verb(role="action", effect="write")
    @require_permission(delegated=["OnlineMeetingRecording.Read.All"], application=["OnlineMeetingRecording.Read.All"])
    def get_all_recordings(
        self,
        meeting_organizer_user_id: str,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> EntityCollection[CallRecording]:
        """Get all recordings from scheduled onlineMeeting instances for which the specified user is the organizer.
        This API currently doesn't support getting call recordings from channel meetings.

        Args:
            meeting_organizer_user_id (str): The user identifier of the meeting organizer to filter for artifacts for
              meetings organized by the given user identifier.
            start_datetime (datetime.datetime): Optional parameter to filter for artifacts created after the given
              start date. The timestamp type represents date and time information using ISO 8601 format and is always
              in UTC
            end_datetime (datetime.datetime): Optional parameter to filter for artifacts created before the given end
              date. The timestamp type represents date and time information using ISO 8601 format and is always in UTC
        """
        return_type = EntityCollection(self.context, CallRecording)
        payload = {
            "meetingOrganizerUserId": meeting_organizer_user_id,
            "startDateTime": start_datetime,
            "endDateTime": end_datetime,
        }
        qry = ServiceOperationQuery(self, "getAllRecordings", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type
