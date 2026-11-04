from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value


@value
class MentionAction(ClientValue):
    mentionees: ClientValueCollection[IdentitySet] = field(default_factory=lambda: ClientValueCollection(IdentitySet))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MentionAction"
