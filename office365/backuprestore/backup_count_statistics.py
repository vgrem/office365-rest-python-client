from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue


class BackupCountStatistics(ClientValue):
    lastComputedDateTime: datetime | None = None
    offboardRequested: int | None = None
    protectedCompleted: int | None = None
    protectedFailed: int | None = None
    protectedInProgress: int | None = None
    removed: int | None = None
    total: int | None = None
    unprotectedCompleted: int | None = None
    unprotectedFailed: int | None = None
    unprotectedInProgress: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BackupCountStatistics"
