from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsAnomalyType(Enum):
    device = "0"
    application = "1"
    stopError = "2"
    driver = "3"
    other = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyType"
