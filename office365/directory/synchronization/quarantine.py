from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.directory.synchronization.error import SynchronizationError
from office365.directory.synchronization.quarantinereason import QuarantineReason
from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationQuarantine(ClientValue):
    """Provides information about the quarantine state of a synchronizationJob.

    Args:
        error (SynchronizationError): Describes the error(s) that occurred when putting the synchronization job
          into quarantine.
    """

    error: SynchronizationError = field(default_factory=SynchronizationError)
    currentBegan: datetime | None = field(default_factory=lambda: datetime.min)
    nextAttempt: datetime | None = field(default_factory=lambda: datetime.min)
    reason: QuarantineReason = QuarantineReason.EncounteredBaseEscrowThreshold
    seriesBegan: datetime | None = field(default_factory=lambda: datetime.min)
    seriesCount: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationQuarantine"
