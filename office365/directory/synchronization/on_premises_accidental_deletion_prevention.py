from __future__ import annotations

from dataclasses import dataclass

from office365.directory.synchronization.onpremisesdeletionpreventiontype import (
    OnPremisesDirectorySynchronizationDeletionPreventionType,
)
from office365.runtime.client_value import ClientValue


@dataclass
class OnPremisesAccidentalDeletionPrevention(ClientValue):
    alertThreshold: int | None = None
    synchronizationPreventionType: OnPremisesDirectorySynchronizationDeletionPreventionType = (
        OnPremisesDirectorySynchronizationDeletionPreventionType.disabled
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesAccidentalDeletionPrevention"
