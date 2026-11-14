from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsDeviceStatus(Enum):
    anomalous = "0"
    affected = "1"
    atRisk = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceStatus"
