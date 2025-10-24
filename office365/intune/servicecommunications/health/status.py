from enum import Enum


class ServiceHealthStatus(Enum):
    serviceOperational = "0"
    investigating = "1"
    restoringService = "2"
    verifyingService = "3"
    serviceRestored = "4"
    postIncidentReviewPublished = "5"
    serviceDegradation = "6"
    serviceInterruption = "7"
    extendedRecovery = "8"
    falsePositive = "9"
    investigationSuspended = "10"
    resolved = "11"
    mitigatedExternal = "12"
    mitigated = "13"
    resolvedExternal = "14"
    confirmed = "15"
    reported = "16"
    unknownFutureValue = "17"

    @property
    def entity_type_name(self):
        return "microsoft.graph.ServiceHealthStatus"
