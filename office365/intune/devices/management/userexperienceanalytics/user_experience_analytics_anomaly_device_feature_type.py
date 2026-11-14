from __future__ import annotations

from enum import Enum


class UserExperienceAnalyticsAnomalyDeviceFeatureType(Enum):
    manufacturer = "0"
    model = "1"
    osVersion = "2"
    application = "3"
    driver = "4"
    unknownFutureValue = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyDeviceFeatureType"
