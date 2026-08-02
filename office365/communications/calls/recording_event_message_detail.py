from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from office365.communications.callrecords.status import CallRecordingStatus
from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class CallRecordingEventMessageDetail(ClientValue):
    callId: str | None = None
    callRecordingDisplayName: str | None = None
    callRecordingDuration: timedelta | None = None
    callRecordingStatus: CallRecordingStatus = CallRecordingStatus.success
    callRecordingUrl: str | None = None
    initiator: IdentitySet = field(default_factory=IdentitySet)
    meetingOrganizer: IdentitySet = field(default_factory=IdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallRecordingEventMessageDetail"
