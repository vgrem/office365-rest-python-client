from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue


@dataclass
class TeamsAppUpgradedEventMessageDetail(ClientValue):
    initiator: IdentitySet = field(default_factory=IdentitySet)
    teamsAppDisplayName: str | None = None
    teamsAppId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamsAppUpgradedEventMessageDetail"
