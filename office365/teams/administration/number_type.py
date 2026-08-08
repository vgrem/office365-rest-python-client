from __future__ import annotations

from enum import Enum


class NumberType(Enum):
    internalError = "0"
    directRouting = "1"
    callingPlan = "2"
    operatorConnect = "3"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.NumberType"
