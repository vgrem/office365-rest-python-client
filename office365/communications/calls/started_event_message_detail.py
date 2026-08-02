from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue
from office365.teams.teamwork.calleventtype import TeamworkCallEventType


@dataclass
class CallStartedEventMessageDetail(ClientValue):
    callEventType: TeamworkCallEventType = TeamworkCallEventType.call
    callId: str | None = None
    initiator: IdentitySet = field(default_factory=IdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CallStartedEventMessageDetail"
