from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class CallTranscriptEventMessageDetail(ClientValue):
    callId: str | None = None
    callTranscriptICalUid: str | None = None
    meetingOrganizer: IdentitySet = field(default_factory=IdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallTranscriptEventMessageDetail"
