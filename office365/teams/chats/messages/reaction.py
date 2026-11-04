from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.chats.messages.reaction_identity_set import ChatMessageReactionIdentitySet


@value
class ChatMessageReaction(ClientValue):
    createdDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    displayName: str | None = None
    reactionContentUrl: str | None = None
    reactionType: str | None = None
    user: ChatMessageReactionIdentitySet = field(default_factory=ChatMessageReactionIdentitySet)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageReaction"
