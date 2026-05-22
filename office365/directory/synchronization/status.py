from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.synchronization.progress import SynchronizationProgress
from office365.directory.synchronization.quarantine import SynchronizationQuarantine
from office365.directory.synchronization.task_execution import (
    SynchronizationTaskExecution,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class SynchronizationStatus(ClientValue):
    """Represents the current status of the synchronizationJob."""

    progress: ClientValueCollection[SynchronizationProgress] = field(
        default_factory=lambda: ClientValueCollection(SynchronizationProgress)
    )
    quarantine: SynchronizationQuarantine = field(default_factory=SynchronizationQuarantine)
    lastExecution: SynchronizationTaskExecution = field(default_factory=SynchronizationTaskExecution)
    lastSuccessfulExecution: SynchronizationTaskExecution = field(default_factory=SynchronizationTaskExecution)
    lastSuccessfulExecutionWithExports: SynchronizationTaskExecution = field(
        default_factory=SynchronizationTaskExecution
    )
