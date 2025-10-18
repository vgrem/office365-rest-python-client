from enum import Enum


class OnPremisesDirectorySynchronizationDeletionPreventionType(Enum):
    disabled = "0"
    enabledForCount = "1"
    enabledForPercentage = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.OnPremisesDirectorySynchronizationDeletionPreventionType"
