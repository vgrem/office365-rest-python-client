from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.teams.chats.messages.citation_sensitivity_label import ChatMessageCitationSensitivityLabel


class ChatMessageCitation(ClientValue):
    excerpt: str | None = None
    iconType: str | None = None
    id: int | None = None
    sensitivityLabel: ChatMessageCitationSensitivityLabel = field(default_factory=ChatMessageCitationSensitivityLabel)
    title: str | None = None
    webUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageCitation"
