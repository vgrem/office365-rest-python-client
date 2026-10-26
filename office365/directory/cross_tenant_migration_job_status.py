from __future__ import annotations

from enum import Enum


class CrossTenantMigrationJobStatus(Enum):
    submitted = "0"
    approved = "1"
    processing = "2"
    cuttingOver = "3"
    inProgress = "4"
    completed = "5"
    completedWithErrors = "6"
    failed = "7"
    cancelled = "8"
    pendingCancel = "9"
    adminActionRequired = "10"
    validateSubmitted = "11"
    validateProcessing = "12"
    validateInProgress = "13"
    validatePassed = "14"
    validateFailed = "15"
    pendingDelete = "16"
    deleted = "17"
    unknownFutureValue = "18"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantMigrationJobStatus"
