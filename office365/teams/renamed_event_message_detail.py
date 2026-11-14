from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.teams.chats.event_message_detail import EventMessageDetail


class TeamRenamedEventMessageDetail(EventMessageDetail):
    initiator: IdentitySet = field(default_factory=IdentitySet)
    teamDisplayName: str | None = None
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamRenamedEventMessageDetail"
