from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.synchronization.error import SynchronizationError
from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationQuarantine(ClientValue):
    """Provides information about the quarantine state of a synchronizationJob.

    Args:
        error (SynchronizationError): Describes the error(s) that occurred when putting the synchronization job into quarantine.
    """

    error: SynchronizationError = field(default_factory=SynchronizationError)
