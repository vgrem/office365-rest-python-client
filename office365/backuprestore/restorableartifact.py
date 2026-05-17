from enum import Enum


class RestorableArtifact(Enum):
    message = "0"
    unknownFutureValue = "1"

    @property
    def entity_type_name(self):
        return "microsoft.graph.RestorableArtifact"
