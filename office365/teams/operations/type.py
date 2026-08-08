from enum import Enum


class TeamsAsyncOperationType(Enum):
    """The type of long-running operation for a team."""

    unknown = "unknown"
    invalid = "invalid"
    cloneTeam = "cloneTeam"
    archiveTeam = "archiveTeam"
    unarchiveTeam = "unarchiveTeam"
    createTeam = "createTeam"
    unknownFutureValue = "unknownFutureValue"
    teamifyGroup = "6"
    createChannel = "7"
    archiveChannel = "8"
    unarchiveChannel = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.teamsAsyncOperationType"
