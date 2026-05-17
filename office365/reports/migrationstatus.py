from enum import Enum


class MigrationStatus(Enum):
    ready = "0"
    needsReview = "1"
    additionalStepsRequired = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self):
        return "microsoft.graph.MigrationStatus"
