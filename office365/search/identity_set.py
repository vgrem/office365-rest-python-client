from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class IdentitySet(ClientValue):
    """Represents a keyed collection of identity resources. It is used to represent a set of
    identities associated with various events for an item, such as created by or last modified by.
    """

    @property
    def entity_type_name(self):
        return "microsoft.graph.search.identitySet"
