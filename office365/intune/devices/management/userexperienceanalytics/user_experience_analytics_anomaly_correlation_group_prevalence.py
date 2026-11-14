from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsAnomalyCorrelationGroupPrevalence(Enum):
    high = "0"
    medium = "1"
    low = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyCorrelationGroupPrevalence"
