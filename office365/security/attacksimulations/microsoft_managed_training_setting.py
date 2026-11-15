from __future__ import annotations

from datetime import datetime

from office365.security.attacksimulations.training_setting import TrainingSetting
from office365.security.attacksimulations.trainingcompletionduration import (
    TrainingCompletionDuration,
)


class MicrosoftManagedTrainingSetting(TrainingSetting):
    completionDateTime: datetime | None = None
    trainingCompletionDuration: TrainingCompletionDuration = TrainingCompletionDuration.week

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftManagedTrainingSetting"
