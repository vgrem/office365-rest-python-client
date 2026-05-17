from enum import Enum


class QuarantineReason(Enum):
    EncounteredBaseEscrowThreshold = "0"
    EncounteredTotalEscrowThreshold = "1"
    EncounteredEscrowProportionThreshold = "2"
    EncounteredQuarantineException = "4"
    Unknown = "8"
    QuarantinedOnDemand = "16"
    TooManyDeletes = "32"
    IngestionInterrupted = "64"

    @property
    def entity_type_name(self):
        return "microsoft.graph.QuarantineReason"
