from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.teams.teamwork.applicationidentitytype import TeamworkApplicationIdentityType


class TeamworkApplicationIdentity(ClientValue):
    applicationIdentityType: TeamworkApplicationIdentityType = TeamworkApplicationIdentityType.aadApplication

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkApplicationIdentity"
