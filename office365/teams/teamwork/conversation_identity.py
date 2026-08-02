from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.teams.teamwork.conversationidentitytype import TeamworkConversationIdentityType


@dataclass
class TeamworkConversationIdentity(ClientValue):
    conversationIdentityType: TeamworkConversationIdentityType = TeamworkConversationIdentityType.team

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkConversationIdentity"
