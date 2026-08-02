from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.teams.chats.messages.actions import ChatMessageActions
from office365.teams.chats.messages.reaction import ChatMessageReaction


@dataclass
class ChatMessageHistoryItem(ClientValue):
    actions: ChatMessageActions = ChatMessageActions.reactionAdded
    modifiedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    reaction: ChatMessageReaction = field(default_factory=ChatMessageReaction)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageHistoryItem"
