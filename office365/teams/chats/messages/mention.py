from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.teams.chats.messages.mentioned_identity_set import ChatMessageMentionedIdentitySet


@dataclass
class ChatMessageMention(ClientValue):
    id: int | None = None
    mentioned: ChatMessageMentionedIdentitySet = field(default_factory=ChatMessageMentionedIdentitySet)
    mentionText: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageMention"
