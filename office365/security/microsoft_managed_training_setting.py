from __future__ import annotations

from datetime import datetime

from office365.security.attacksimulations.trainingcompletionduration import (
    TrainingCompletionDuration,
)
from office365.security.training_setting import TrainingSetting


class MicrosoftManagedTrainingSetting(TrainingSetting):
    completionDateTime: datetime | None = None
    trainingCompletionDuration: TrainingCompletionDuration = TrainingCompletionDuration.week

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftManagedTrainingSetting"
