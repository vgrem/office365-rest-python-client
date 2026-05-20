from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SynchronizationProgress(ClientValue):
    """
    Represents the progress of a synchronizationJob toward completion.
    """

    completedUnits: str | None = None
    progressObservationDateTime: str | None = None
    totalUnits: str | None = None
    units: str | None = None
