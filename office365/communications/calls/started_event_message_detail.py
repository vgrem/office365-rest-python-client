from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.teams.chats.event_message_detail import EventMessageDetail
from office365.teams.teamwork.calleventtype import TeamworkCallEventType


class CallStartedEventMessageDetail(EventMessageDetail):
    callEventType: TeamworkCallEventType = TeamworkCallEventType.call
    callId: str | None = None
    initiator: IdentitySet = field(default_factory=IdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallStartedEventMessageDetail"
