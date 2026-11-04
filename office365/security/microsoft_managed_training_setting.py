from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.attacksimulations.trainingcompletionduration import (
    TrainingCompletionDuration,
)


@value
class MicrosoftManagedTrainingSetting(ClientValue):
    completionDateTime: datetime | None = None
    trainingCompletionDuration: TrainingCompletionDuration = TrainingCompletionDuration.week

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftManagedTrainingSetting"
