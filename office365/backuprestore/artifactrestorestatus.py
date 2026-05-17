from enum import Enum


class ArtifactRestoreStatus(Enum):
    added = "0"
    scheduling = "1"
    scheduled = "2"
    inProgress = "3"
    succeeded = "4"
    failed = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ArtifactRestoreStatus"
