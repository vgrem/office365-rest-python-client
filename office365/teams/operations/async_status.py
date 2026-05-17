from enum import Enum


class TeamsAsyncOperationStatus(Enum):
    """Describes the current status of a teamsAsyncOperation."""

    invalid = 0
    "\tInvalid value."
    notStarted = 1
    "The operation has not started."
    inProgress = 2
    "\tThe operation is running."
    succeeded = 3
    "The operation succeeded."
    failed = 4
    "The operation failed."
    unknownFutureValue = "5"

    @property
    def entity_type_name(self):
        return "microsoft.graph.TeamsAsyncOperationStatus"
