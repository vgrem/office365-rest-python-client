from __future__ import annotations

from dataclasses import field

from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_device_feature_type import (  # noqa: E501
    UserExperienceAnalyticsAnomalyDeviceFeatureType,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class UserExperienceAnalyticsAnomalyCorrelationGroupFeature(ClientValue):
    deviceFeatureType: UserExperienceAnalyticsAnomalyDeviceFeatureType = (
        UserExperienceAnalyticsAnomalyDeviceFeatureType.manufacturer
    )
    values: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyCorrelationGroupFeature"
