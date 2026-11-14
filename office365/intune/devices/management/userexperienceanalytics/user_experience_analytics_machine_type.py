from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsMachineType(Enum):
    unknown = "0"
    physical = "1"
    virtual = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsMachineType"
