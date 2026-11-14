from office365.directory.permissions.identity import Identity


class TeamworkTagIdentity(Identity):
    """Represents a tag in Microsoft Teams. Tags allow users to quickly connect to subset of users in a team.
    For details about tag management in Microsoft Teams, see Manage tags in Microsoft Teams.
    """

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TeamworkTagIdentity"
