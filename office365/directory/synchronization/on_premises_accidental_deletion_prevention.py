from __future__ import annotations

from office365.directory.synchronization.onpremisesdeletionpreventiontype import (
    OnPremisesDirectorySynchronizationDeletionPreventionType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class OnPremisesAccidentalDeletionPrevention(ClientValue):
    alertThreshold: int | None = None
    synchronizationPreventionType: OnPremisesDirectorySynchronizationDeletionPreventionType = (
        OnPremisesDirectorySynchronizationDeletionPreventionType.disabled
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesAccidentalDeletionPrevention"
