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

    @property
    def entity_type_name(self):
        return "microsoft.graph.teamsAsyncOperationType"
