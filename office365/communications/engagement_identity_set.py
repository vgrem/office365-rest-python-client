from __future__ import annotations

from dataclasses import field

from office365.directory.identity_set import IdentitySet
from office365.directory.permissions.identity import Identity


class EngagementIdentitySet(IdentitySet):
    audience: Identity = field(default_factory=Identity)
    group: Identity = field(default_factory=Identity)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EngagementIdentitySet"
