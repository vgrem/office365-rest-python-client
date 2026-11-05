from __future__ import annotations

from dataclasses import field

from office365.directory.permissions.identity_set import IdentitySet
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.teams.teamwork.user_identity import TeamworkUserIdentity


class MembersLeftEventMessageDetail(ClientValue):
    initiator: IdentitySet = field(default_factory=IdentitySet)
    members: ClientValueCollection[TeamworkUserIdentity] = field(
        default_factory=lambda: ClientValueCollection(TeamworkUserIdentity)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MembersLeftEventMessageDetail"
