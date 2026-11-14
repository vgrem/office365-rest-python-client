from __future__ import annotations

from office365.directory.identity_set import IdentitySet


class ChatMessageReactionIdentitySet(IdentitySet):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageReactionIdentitySet"
