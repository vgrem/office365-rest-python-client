from office365.directory.permissions.identity import Identity
from office365.teams.teamwork.useridentitytype import TeamworkUserIdentityType


class TeamworkUserIdentity(Identity):
    userIdentityType: TeamworkUserIdentityType = TeamworkUserIdentityType.aadUser
    "Represents a user in Microsoft Teams."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkUserIdentity"
