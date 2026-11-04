from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.chats.messages.mentioned_identity_set import ChatMessageMentionedIdentitySet


@value
class ChatMessageMention(ClientValue):
    id: int | None = None
    mentioned: ChatMessageMentionedIdentitySet = field(default_factory=ChatMessageMentionedIdentitySet)
    mentionText: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageMention"
