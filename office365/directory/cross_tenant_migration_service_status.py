from __future__ import annotations

from enum import Enum


class CrossTenantMigrationServiceStatus(Enum):
    notStarted = "0"
    valid = "1"
    invalid = "2"
    error = "3"
    inProgress = "4"
    completed = "5"
    failed = "6"
    cancelled = "7"
    pendingCancel = "8"
    syncing = "9"
    synced = "10"
    finalizing = "11"
    forceComplete = "12"
    unknownFutureValue = "13"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CrossTenantMigrationServiceStatus"
