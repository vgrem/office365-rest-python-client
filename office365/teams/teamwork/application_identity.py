from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.teams.teamwork.applicationidentitytype import TeamworkApplicationIdentityType


@value
class TeamworkApplicationIdentity(ClientValue):
    applicationIdentityType: TeamworkApplicationIdentityType = TeamworkApplicationIdentityType.aadApplication

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkApplicationIdentity"
