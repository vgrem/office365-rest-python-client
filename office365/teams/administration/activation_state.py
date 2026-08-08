from __future__ import annotations

from enum import Enum


class ActivationState(Enum):
    activated = "0"
    assignmentPending = "1"
    assignmentFailed = "2"
    updatePending = "3"
    updateFailed = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.ActivationState"
