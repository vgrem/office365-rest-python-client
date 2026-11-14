from __future__ import annotations

from office365.directory.permissions.identity import Identity
from office365.teams.teamwork.applicationidentitytype import TeamworkApplicationIdentityType


class TeamworkApplicationIdentity(Identity):
    applicationIdentityType: TeamworkApplicationIdentityType = TeamworkApplicationIdentityType.aadApplication

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkApplicationIdentity"
