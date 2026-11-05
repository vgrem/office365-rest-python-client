from __future__ import annotations

from office365.directory.synchronization.onpremisesdeletionpreventiontype import (
    OnPremisesDirectorySynchronizationDeletionPreventionType,
)
from office365.runtime.client_value import ClientValue


class OnPremisesAccidentalDeletionPrevention(ClientValue):
    alertThreshold: int | None = None
    synchronizationPreventionType: OnPremisesDirectorySynchronizationDeletionPreventionType = (
        OnPremisesDirectorySynchronizationDeletionPreventionType.disabled
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesAccidentalDeletionPrevention"
