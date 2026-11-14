from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsAnomalySeverity(Enum):
    high = "0"
    medium = "1"
    low = "2"
    informational = "3"
    other = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalySeverity"
