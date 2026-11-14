from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_correlation_group_feature import (  # noqa: E501
    UserExperienceAnalyticsAnomalyCorrelationGroupFeature,
)
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_correlation_group_prevalence import (  # noqa: E501
    UserExperienceAnalyticsAnomalyCorrelationGroupPrevalence,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsAnomalyCorrelationGroupOverview(Entity):
    @odata(name="anomalyCorrelationGroupCount")
    @property
    def anomaly_correlation_group_count(self) -> Optional[int]:
        """Gets the anomalyCorrelationGroupCount property"""
        return self.properties.get("anomalyCorrelationGroupCount", None)

    @odata(name="anomalyId")
    @property
    def anomaly_id(self) -> Optional[str]:
        """Gets the anomalyId property"""
        return self.properties.get("anomalyId", None)

    @odata(name="correlationGroupAnomalousDeviceCount")
    @property
    def correlation_group_anomalous_device_count(self) -> Optional[int]:
        """Gets the correlationGroupAnomalousDeviceCount property"""
        return self.properties.get("correlationGroupAnomalousDeviceCount", None)

    @odata(name="correlationGroupAtRiskDeviceCount")
    @property
    def correlation_group_at_risk_device_count(self) -> Optional[int]:
        """Gets the correlationGroupAtRiskDeviceCount property"""
        return self.properties.get("correlationGroupAtRiskDeviceCount", None)

    @odata(name="correlationGroupDeviceCount")
    @property
    def correlation_group_device_count(self) -> Optional[int]:
        """Gets the correlationGroupDeviceCount property"""
        return self.properties.get("correlationGroupDeviceCount", None)

    @odata(name="correlationGroupFeatures")
    @property
    def correlation_group_features(self) -> ClientValueCollection[UserExperienceAnalyticsAnomalyCorrelationGroupFeature]:
        """Gets the correlationGroupFeatures property"""
        return self.properties.get(
            "correlationGroupFeatures",
            ClientValueCollection[UserExperienceAnalyticsAnomalyCorrelationGroupFeature](
                UserExperienceAnalyticsAnomalyCorrelationGroupFeature
            ),
        )

    @odata(name="correlationGroupId")
    @property
    def correlation_group_id(self) -> Optional[str]:
        """Gets the correlationGroupId property"""
        return self.properties.get("correlationGroupId", None)

    @odata(name="correlationGroupPrevalence")
    @property
    def correlation_group_prevalence(self) -> Optional[UserExperienceAnalyticsAnomalyCorrelationGroupPrevalence]:
        """Gets the correlationGroupPrevalence property"""
        return self.properties.get("correlationGroupPrevalence", None)

    @odata(name="correlationGroupPrevalencePercentage")
    @property
    def correlation_group_prevalence_percentage(self) -> Optional[float]:
        """Gets the correlationGroupPrevalencePercentage property"""
        return self.properties.get("correlationGroupPrevalencePercentage", None)

    @odata(name="totalDeviceCount")
    @property
    def total_device_count(self) -> Optional[int]:
        """Gets the totalDeviceCount property"""
        return self.properties.get("totalDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomalyCorrelationGroupOverview"
