from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class TeamRenamedEventMessageDetail(ClientValue):
    initiator: IdentitySet = field(default_factory=IdentitySet)
    teamDisplayName: str | None = None
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamRenamedEventMessageDetail"
