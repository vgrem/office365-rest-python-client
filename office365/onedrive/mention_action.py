from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class MentionAction(ClientValue):
    mentionees: ClientValueCollection[IdentitySet] = field(default_factory=lambda: ClientValueCollection(IdentitySet))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MentionAction"
