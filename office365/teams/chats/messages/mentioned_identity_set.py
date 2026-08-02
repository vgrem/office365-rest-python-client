from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.teamwork.conversation_identity import TeamworkConversationIdentity


@dataclass
class ChatMessageMentionedIdentitySet(ClientValue):
    conversation: TeamworkConversationIdentity = field(default_factory=TeamworkConversationIdentity)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageMentionedIdentitySet"
