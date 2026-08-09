from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.synchronization.on_premises_accidental_deletion_prevention import (
    OnPremisesAccidentalDeletionPrevention,
)
from office365.runtime.client_value import ClientValue


@dataclass
class OnPremisesDirectorySynchronizationConfiguration(ClientValue):
    accidentalDeletionPrevention: OnPremisesAccidentalDeletionPrevention = field(
        default_factory=OnPremisesAccidentalDeletionPrevention
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnPremisesDirectorySynchronizationConfiguration"
