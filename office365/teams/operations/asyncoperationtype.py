from enum import Enum


class TeamsAsyncOperationType(Enum):
    invalid = "0"
    cloneTeam = "1"
    archiveTeam = "2"
    unarchiveTeam = "3"
    createTeam = "4"
    unknownFutureValue = "5"
    teamifyGroup = "6"
    createChannel = "7"
    archiveChannel = "8"
    unarchiveChannel = "9"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamsAsyncOperationType"
