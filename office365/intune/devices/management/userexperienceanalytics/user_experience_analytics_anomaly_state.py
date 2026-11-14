from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsAnomalyState(Enum):
    new = "0"
    active = "1"
    disabled = "2"
    removed = "3"
    other = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyState"
