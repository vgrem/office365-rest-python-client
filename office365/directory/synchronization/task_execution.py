from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.directory.synchronization.error import SynchronizationError
from office365.directory.synchronization.taskexecutionresult import SynchronizationTaskExecutionResult
from office365.runtime.client_value import ClientValue


class SynchronizationTaskExecution(ClientValue):
    activityIdentifier: str | None = None
    countEntitled: int | None = None
    countEntitledForProvisioning: int | None = None
    countEscrowed: int | None = None
    countEscrowedRaw: int | None = None
    countExported: int | None = None
    countExports: int | None = None
    countImported: int | None = None
    countImportedDeltas: int | None = None
    countImportedReferenceDeltas: int | None = None
    error: SynchronizationError = field(default_factory=SynchronizationError)
    state: SynchronizationTaskExecutionResult = SynchronizationTaskExecutionResult.Succeeded
    timeBegan: datetime | None = field(default_factory=lambda: datetime.min)
    timeEnded: datetime | None = field(default_factory=lambda: datetime.min)
    "Summarizes the results of the synchronization job run."

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationTaskExecution"
