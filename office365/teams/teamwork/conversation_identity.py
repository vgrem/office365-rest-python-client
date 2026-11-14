from __future__ import annotations

from office365.directory.permissions.identity import Identity
from office365.teams.teamwork.conversationidentitytype import TeamworkConversationIdentityType


class TeamworkConversationIdentity(Identity):
    conversationIdentityType: TeamworkConversationIdentityType = TeamworkConversationIdentityType.team

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkConversationIdentity"
