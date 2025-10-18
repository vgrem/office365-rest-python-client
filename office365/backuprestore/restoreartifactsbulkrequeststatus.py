from enum import Enum


class RestoreArtifactsBulkRequestStatus(Enum):
    unknown = "0"
    active = "1"
    completed = "2"
    completedWithErrors = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RestoreArtifactsBulkRequestStatus"
