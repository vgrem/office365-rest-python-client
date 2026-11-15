from __future__ import annotations

from office365.directory.identities.set import IdentitySet


class ChatMessageFromIdentitySet(IdentitySet):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageFromIdentitySet"
