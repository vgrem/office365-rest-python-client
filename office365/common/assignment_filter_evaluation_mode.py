from __future__ import annotations

from enum import Enum


class AssignmentFilterEvaluationMode(Enum):
    checkinTimeEvaluation = "0"
    inventoryEvaluation = "1"
    mixedEvaluation = "2"
    disabled = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AssignmentFilterEvaluationMode"
