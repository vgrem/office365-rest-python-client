from __future__ import annotations

from office365.directory.permissions.identity import Identity
from office365.teams.teamwork.useridentitytype import TeamworkUserIdentityType


class TeamworkUserIdentity(Identity):
    userIdentityType: TeamworkUserIdentityType = TeamworkUserIdentityType.aadUser
    userPrincipalName: str | None = None
    "Represents a user in Microsoft Teams."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkUserIdentity"
