from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class CommentAction(ClientValue):
    isReply: bool | None = None
    parentAuthor: IdentitySet = field(default_factory=IdentitySet)
    participants: ClientValueCollection[IdentitySet] = field(default_factory=lambda: ClientValueCollection(IdentitySet))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CommentAction"
