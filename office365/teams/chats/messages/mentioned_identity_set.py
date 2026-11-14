from __future__ import annotations

from dataclasses import field

from office365.directory.identity_set import IdentitySet
from office365.teams.teamwork.conversation_identity import TeamworkConversationIdentity


class ChatMessageMentionedIdentitySet(IdentitySet):
    conversation: TeamworkConversationIdentity = field(default_factory=TeamworkConversationIdentity)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageMentionedIdentitySet"
