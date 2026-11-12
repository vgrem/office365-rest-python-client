from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.communications.callrecords.modality import Modality
from office365.communications.calls.direction import CallDirection
from office365.communications.calls.incoming_context import IncomingContext
from office365.communications.calls.invitation_participant_info import (
    InvitationParticipantInfo,
)
from office365.communications.calls.media_state import CallMediaState
from office365.communications.calls.options import CallOptions
from office365.communications.calls.participant import Participant
from office365.communications.calls.participant_info import ParticipantInfo
from office365.communications.calls.route import CallRoute
from office365.communications.calls.state import CallState
from office365.communications.calls.transcription_info import CallTranscriptionInfo
from office365.communications.media_config import MediaConfig
from office365.communications.meetings.info import MeetingInfo
from office365.communications.onlinemeetings.collection import ChatInfo
from office365.communications.operations.cancel_media_processing import (
    CancelMediaProcessingOperation,
)
from office365.communications.operations.comms import CommsOperation
from office365.communications.operations.unmute_participant import (
    UnmuteParticipantOperation,
)
from office365.communications.operations.update_recording_status import (
    UpdateRecordingStatusOperation,
)
from office365.communications.quotas import CALL_QUOTAS
from office365.communications.result_info import ResultInfo
from office365.communications.tone_info import ToneInfo
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.limits import limit
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.common.add_large_gallery_view_operation import AddLargeGalleryViewOperation
    from office365.common.mute_participant_operation import MuteParticipantOperation
    from office365.common.play_prompt_operation import PlayPromptOperation
    from office365.common.prompt import Prompt
    from office365.common.record_operation import RecordOperation
    from office365.common.subscribe_to_tone_operation import SubscribeToToneOperation
    from office365.communications.calls.audio_routing_group import AudioRoutingGroup
    from office365.communications.calls.content_sharing_session import (
        ContentSharingSession,
    )
    from office365.communications.calls.screensharingrole import ScreenSharingRole
    from office365.communications.calls.tone import Tone
    from office365.communications.incoming_call_options import IncomingCallOptions
    from office365.communications.send_dtmf_tones_operation import SendDtmfTonesOperation


@limit(*CALL_QUOTAS)
class Call(Entity):
    """
    The call resource is created when there is an incoming call for the application or the application creates a
    new outgoing call via a POST on app/calls.
    """

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def cancel_media_processing(self, client_context=None):
        """Cancels processing for any in-progress media operations.

        Media operations refer to the IVR operations playPrompt and recordResponse, which are by default queued
        to process in order. The cancelMediaProcessing method cancels any operation that is in-process as well as
        operations that are queued. For example, this method can be used to clean up the IVR operation queue for
        a new media operation. However, it will not cancel a subscribeToTone operation because it operates independent
        of any operation queue.

        Args:
            client_context (str): The client context.
        """
        return_type = CancelMediaProcessingOperation(self.context)
        payload = {"clientContext": client_context}
        qry = ServiceOperationQuery(self, "cancelMediaProcessing", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def reject(self, reason=None, callback_uri=None):
        """Enable a bot to reject an incoming call. The incoming call request can be an invite from a participant in
        a group call or a peer-to-peer call. If an invite to a group call is received, the notification will contain
        the chatInfo and meetingInfo parameters.

        The bot is expected to answer or reject the call before the call times out. The current timeout value is
        15 seconds.

        This API does not end existing calls that have already been answered. Use delete call to end a call.

        Args:
            reason (str): The rejection reason. Possible values are None, Busy and Forbidden
            callback_uri (str): This allows bots to provide a specific callback URI for the current call to receive
            later notifications. If this property has not been set, the bot's global callback URI will be used instead.
             This must be https.
        """
        payload = {"reason": reason, "callbackUri": callback_uri}
        qry = ServiceOperationQuery(self, "reject", None, payload)
        self.context.add_query(qry)
        return self

    def delete(self):
        """
        Delete or hang up an active call. For group calls, this will only delete your call leg and the underlying
        group call will still continue."""
        return super().delete_object()

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def update_recording_status(self, status, client_context):
        """Update the application's recording status associated with a call.
        This requires the use of the Teams policy-based recording solution.

        Args:
            status (str): The recording status. Possible values are: notRecording, recording, or failed.
            client_context (str): Unique client context string. Max limit is 256 chars.
        """
        return_type = UpdateRecordingStatusOperation(self.context)
        payload = {"status": status, "clientContext": client_context}
        qry = ServiceOperationQuery(self, "updateRecordingStatus", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def unmute(self, client_context):
        """Allow the application to unmute itself.

        This is a server unmute, meaning that the server will start sending audio packets for this participant
        to other participants again.

        Args:
            client_context (str): Unique Client Context string. Max limit is 256 chars.
        """
        return_type = UnmuteParticipantOperation(self.context)
        payload = {"clientContext": client_context}
        qry = ServiceOperationQuery(self, "unmute", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @odata(name="callbackUri")
    @property
    def callback_uri(self) -> Optional[str]:
        """The callback URL on which callbacks will be delivered. Must be https."""
        return self.properties.get("callbackUri", None)

    @odata(name="callRoutes")
    @property
    def call_routes(self) -> ClientValueCollection[CallRoute]:
        """The routing information on how the call was retargeted. Read-only."""
        return self.properties.get("callRoutes", ClientValueCollection(CallRoute))

    @odata(name="incomingContext")
    @property
    def incoming_context(self) -> IncomingContext:
        """Call context associated with an incoming call."""
        return self.properties.get("incomingContext", IncomingContext())

    @odata(name="participants", navigation=True)
    @property
    def participants(self):
        """
        Participant collection
        """
        return self.properties.get(
            "participants", EntityCollection(self.context, Participant, ResourcePath("participants", self.resource_path))
        )

    @odata(name="operations", navigation=True)
    @property
    def operations(self):
        """
        CommsOperation collection
        """
        return self.properties.get(
            "operations", EntityCollection(self.context, CommsOperation, ResourcePath("operations", self.resource_path))
        )

    @odata(name="callChainId")
    @property
    def call_chain_id(self) -> Optional[str]:
        """Gets the callChainId property"""
        return self.properties.get("callChainId", None)

    @odata(name="callOptions")
    @property
    def call_options(self) -> CallOptions:
        """Gets the callOptions property"""
        return self.properties.get("callOptions", CallOptions())

    @odata(name="chatInfo")
    @property
    def chat_info(self) -> ChatInfo:
        """Gets the chatInfo property"""
        return self.properties.get("chatInfo", ChatInfo())

    @odata(name="direction")
    @property
    def direction(self) -> CallDirection:
        """Gets the direction property"""
        return self.properties.get("direction", CallDirection.incoming)

    @odata(name="meetingInfo")
    @property
    def meeting_info(self) -> MeetingInfo:
        """Gets the meetingInfo property"""
        return self.properties.get("meetingInfo", MeetingInfo())

    @odata(name="myParticipantId")
    @property
    def my_participant_id(self) -> Optional[str]:
        """Gets the myParticipantId property"""
        return self.properties.get("myParticipantId", None)

    @odata(name="requestedModalities")
    @property
    def requested_modalities(self) -> ClientValueCollection[Modality]:
        """Gets the requestedModalities property"""
        return self.properties.get("requestedModalities", ClientValueCollection[Modality](Modality))

    @odata(name="resultInfo")
    @property
    def result_info(self) -> ResultInfo:
        """Gets the resultInfo property"""
        return self.properties.get("resultInfo", ResultInfo())

    @odata(name="source")
    @property
    def source(self) -> ParticipantInfo:
        """Gets the source property"""
        return self.properties.get("source", ParticipantInfo())

    @odata(name="state")
    @property
    def state(self) -> CallState:
        """Gets the state property"""
        return self.properties.get("state", CallState.incoming)

    @odata(name="subject")
    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @odata(name="targets")
    @property
    def targets(self) -> ClientValueCollection[InvitationParticipantInfo]:
        """Gets the targets property"""
        return self.properties.get(
            "targets", ClientValueCollection[InvitationParticipantInfo](InvitationParticipantInfo)
        )

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Call"

    @odata(name="mediaConfig")
    @property
    def media_config(self) -> MediaConfig:
        """Gets the mediaConfig property"""
        return self.properties.get("mediaConfig", MediaConfig())

    @odata(name="mediaState")
    @property
    def media_state(self) -> CallMediaState:
        """Gets the mediaState property"""
        return self.properties.get("mediaState", CallMediaState())

    @odata(name="toneInfo")
    @property
    def tone_info(self) -> ToneInfo:
        """Gets the toneInfo property"""
        return self.properties.get("toneInfo", ToneInfo())

    @odata(name="transcription")
    @property
    def transcription(self) -> CallTranscriptionInfo:
        """Gets the transcription property"""
        return self.properties.get("transcription", CallTranscriptionInfo())

    @odata(name="audioRoutingGroups", navigation=True)
    @property
    def audio_routing_groups(self) -> EntityCollection[AudioRoutingGroup]:
        """Gets the audioRoutingGroups property"""
        from office365.communications.calls.audio_routing_group import AudioRoutingGroup

        return self.properties.get(
            "audioRoutingGroups",
            EntityCollection[AudioRoutingGroup](
                self.context, AudioRoutingGroup, ResourcePath("audioRoutingGroups", self.resource_path)
            ),
        )

    @odata(name="contentSharingSessions", navigation=True)
    @property
    def content_sharing_sessions(self) -> EntityCollection[ContentSharingSession]:
        """Gets the contentSharingSessions property"""
        from office365.communications.calls.content_sharing_session import (
            ContentSharingSession,
        )

        return self.properties.get(
            "contentSharingSessions",
            EntityCollection[ContentSharingSession](
                self.context, ContentSharingSession, ResourcePath("contentSharingSessions", self.resource_path)
            ),
        )

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.Initiate.All"])
    def redirect(
        self, targets: ClientValueCollection[InvitationParticipantInfo], timeout: int, callback_uri: str
    ) -> Self:
        """redirect operation.

        Args:
            targets (ClientValueCollection[InvitationParticipantInfo]):
                targets parameter
            timeout (int):
                timeout parameter
            callback_uri (str):
                callbackUri parameter
        """
        qry = ServiceOperationQuery(
            self, "redirect", None, {"targets": targets, "timeout": timeout, "callbackUri": callback_uri}, None, None
        )
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        application=["Calls.JoinGroupCallAsGuest.All", "Calls.InitiateGroupCall.All", "Calls.JoinGroupCall.All"],
    )
    def add_large_gallery_view(self, client_context: str) -> AddLargeGalleryViewOperation:
        """addLargeGalleryView operation.

        Args:
            client_context (str):
                clientContext parameter
        """
        from office365.common.add_large_gallery_view_operation import AddLargeGalleryViewOperation

        return_type = AddLargeGalleryViewOperation(self.context)
        qry = ServiceOperationQuery(
            self, "addLargeGalleryView", None, {"clientContext": client_context}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.JoinGroupCall.All", "Calls.JoinGroupCallAsGuest.All"])
    def answer(
        self,
        callback_uri: str,
        media_config: MediaConfig,
        accepted_modalities: ClientValueCollection[Modality],
        participant_capacity: int,
        call_options: IncomingCallOptions,
    ) -> Self:
        """answer operation.

        Args:
            callback_uri (str):
                callbackUri parameter
            media_config (MediaConfig):
                mediaConfig parameter
            accepted_modalities (ClientValueCollection[Modality]):
                acceptedModalities parameter
            participant_capacity (int):
                participantCapacity parameter
            call_options (IncomingCallOptions):
                callOptions parameter
        """
        qry = ServiceOperationQuery(
            self,
            "answer",
            None,
            {
                "callbackUri": callback_uri,
                "mediaConfig": media_config,
                "acceptedModalities": accepted_modalities,
                "participantCapacity": participant_capacity,
                "callOptions": call_options,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def change_screen_sharing_role(self, role: ScreenSharingRole) -> Self:
        """changeScreenSharingRole operation.

        Args:
            role (ScreenSharingRole):
                role parameter
        """
        qry = ServiceOperationQuery(self, "changeScreenSharingRole", None, {"role": role}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.Initiate.All", "Calls.AccessMedia.All"])
    def keep_alive(self) -> Self:
        """keepAlive operation."""
        qry = ServiceOperationQuery(self, "keepAlive", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.Initiate.All", "Calls.AccessMedia.All"])
    def mute(self, client_context: str) -> MuteParticipantOperation:
        """mute operation.

        Args:
            client_context (str):
                clientContext parameter
        """
        from office365.common.mute_participant_operation import MuteParticipantOperation

        return_type = MuteParticipantOperation(self.context)
        qry = ServiceOperationQuery(self, "mute", None, {"clientContext": client_context}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.Initiate.All", "Calls.AccessMedia.All"])
    def play_prompt(self, prompts: ClientValueCollection[Prompt], client_context: str) -> PlayPromptOperation:
        """playPrompt operation.

        Args:
            prompts (ClientValueCollection[Prompt]):
                prompts parameter
            client_context (str):
                clientContext parameter
        """
        from office365.common.play_prompt_operation import PlayPromptOperation

        return_type = PlayPromptOperation(self.context)
        qry = ServiceOperationQuery(
            self, "playPrompt", None, {"prompts": prompts, "clientContext": client_context}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def record_response(
        self,
        prompts: ClientValueCollection[Prompt],
        barge_in_allowed: bool,
        initial_silence_timeout_in_seconds: int,
        max_silence_timeout_in_seconds: int,
        max_record_duration_in_seconds: int,
        play_beep: bool,
        stop_tones: list[str],
        client_context: str,
    ) -> RecordOperation:
        """recordResponse operation.

        Args:
            prompts (ClientValueCollection[Prompt]):
                prompts parameter
            barge_in_allowed (bool):
                bargeInAllowed parameter
            initial_silence_timeout_in_seconds (int):
                initialSilenceTimeoutInSeconds parameter
            max_silence_timeout_in_seconds (int):
                maxSilenceTimeoutInSeconds parameter
            max_record_duration_in_seconds (int):
                maxRecordDurationInSeconds parameter
            play_beep (bool):
                playBeep parameter
            stop_tones (list[str]):
                stopTones parameter
            client_context (str):
                clientContext parameter
        """
        from office365.common.record_operation import RecordOperation

        return_type = RecordOperation(self.context)
        qry = ServiceOperationQuery(
            self,
            "recordResponse",
            None,
            {
                "prompts": prompts,
                "bargeInAllowed": barge_in_allowed,
                "initialSilenceTimeoutInSeconds": initial_silence_timeout_in_seconds,
                "maxSilenceTimeoutInSeconds": max_silence_timeout_in_seconds,
                "maxRecordDurationInSeconds": max_record_duration_in_seconds,
                "playBeep": play_beep,
                "stopTones": StringCollection(stop_tones),
                "clientContext": client_context,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.Initiate.All", "Calls.AccessMedia.All"])
    def send_dtmf_tones(
        self, tones: ClientValueCollection[Tone], delay_between_tones_ms: int, client_context: str
    ) -> SendDtmfTonesOperation:
        """sendDtmfTones operation.

        Args:
            tones (ClientValueCollection[Tone]):
                tones parameter
            delay_between_tones_ms (int):
                delayBetweenTonesMs parameter
            client_context (str):
                clientContext parameter
        """
        from office365.communications.send_dtmf_tones_operation import SendDtmfTonesOperation

        return_type = SendDtmfTonesOperation(self.context)
        qry = ServiceOperationQuery(
            self,
            "sendDtmfTones",
            None,
            {"tones": tones, "delayBetweenTonesMs": delay_between_tones_ms, "clientContext": client_context},
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.AccessMedia.All"])
    def subscribe_to_tone(self, client_context: str) -> SubscribeToToneOperation:
        """subscribeToTone operation.

        Args:
            client_context (str):
                clientContext parameter
        """
        from office365.common.subscribe_to_tone_operation import SubscribeToToneOperation

        return_type = SubscribeToToneOperation(self.context)
        qry = ServiceOperationQuery(self, "subscribeToTone", None, {"clientContext": client_context}, None, return_type)
        self.context.add_query(qry)
        return return_type

    @verb(role="action", effect="write")
    @require_permission(application=["Calls.Initiate.All"])
    def transfer(self, transfer_target: InvitationParticipantInfo, transferee: ParticipantInfo) -> Self:
        """transfer operation.

        Args:
            transfer_target (InvitationParticipantInfo):
                transferTarget parameter
            transferee (ParticipantInfo):
                transferee parameter
        """
        qry = ServiceOperationQuery(
            self, "transfer", None, {"transferTarget": transfer_target, "transferee": transferee}, None, None
        )
        self.context.add_query(qry)
        return self
