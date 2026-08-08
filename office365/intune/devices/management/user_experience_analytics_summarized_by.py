from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsSummarizedBy(Enum):
    none = "0"
    model = "1"
    allRegressions = "3"
    modelRegression = "4"
    manufacturerRegression = "5"
    operatingSystemVersionRegression = "6"
    unknownFutureValue = "7"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsSummarizedBy"
