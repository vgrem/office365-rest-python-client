from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.attacksimulations.trainingassignedto import (
    TrainingAssignedTo,
)
from office365.security.training_setting import TrainingSetting


class CustomTrainingSetting(TrainingSetting):
    assignedTo: ClientValueCollection[TrainingAssignedTo] = field(
        default_factory=lambda: ClientValueCollection(TrainingAssignedTo)
    )
    description: str | None = None
    displayName: str | None = None
    durationInMinutes: int | None = None
    url: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CustomTrainingSetting"
