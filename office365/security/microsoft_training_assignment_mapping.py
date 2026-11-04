from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.security.attacksimulations.trainingassignedto import (
    TrainingAssignedTo,
)

if TYPE_CHECKING:
    from office365.security.training import Training


@value
class MicrosoftTrainingAssignmentMapping(ClientValue):
    assignedTo: ClientValueCollection[TrainingAssignedTo] = field(
        default_factory=lambda: ClientValueCollection(TrainingAssignedTo)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTrainingAssignmentMapping"

    training: Training | None = None
