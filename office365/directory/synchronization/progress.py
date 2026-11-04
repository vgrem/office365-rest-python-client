from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SynchronizationProgress(ClientValue):
    """
    Represents the progress of a synchronizationJob toward completion.
    """

    completedUnits: str | None = None
    progressObservationDateTime: str | None = None
    totalUnits: str | None = None
    units: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SynchronizationProgress"
