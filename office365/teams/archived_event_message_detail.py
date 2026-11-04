from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TeamArchivedEventMessageDetail(ClientValue):
    initiator: IdentitySet = field(default_factory=IdentitySet)
    teamId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamArchivedEventMessageDetail"
