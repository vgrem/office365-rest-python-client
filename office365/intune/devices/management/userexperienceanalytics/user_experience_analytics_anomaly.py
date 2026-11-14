from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_severity import (
    UserExperienceAnalyticsAnomalySeverity,
)
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_state import (
    UserExperienceAnalyticsAnomalyState,
)
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_type import (
    UserExperienceAnalyticsAnomalyType,
)
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsAnomaly(Entity):
    @odata(name="anomalyFirstOccurrenceDateTime")
    @property
    def anomaly_first_occurrence_date_time(self) -> Optional[datetime]:
        """Gets the anomalyFirstOccurrenceDateTime property"""
        return self.properties.get("anomalyFirstOccurrenceDateTime", None)

    @odata(name="anomalyId")
    @property
    def anomaly_id(self) -> Optional[str]:
        """Gets the anomalyId property"""
        return self.properties.get("anomalyId", None)

    @odata(name="anomalyLatestOccurrenceDateTime")
    @property
    def anomaly_latest_occurrence_date_time(self) -> Optional[datetime]:
        """Gets the anomalyLatestOccurrenceDateTime property"""
        return self.properties.get("anomalyLatestOccurrenceDateTime", None)

    @odata(name="anomalyName")
    @property
    def anomaly_name(self) -> Optional[str]:
        """Gets the anomalyName property"""
        return self.properties.get("anomalyName", None)

    @odata(name="anomalyType")
    @property
    def anomaly_type(self) -> Optional[UserExperienceAnalyticsAnomalyType]:
        """Gets the anomalyType property"""
        return self.properties.get("anomalyType", None)

    @odata(name="assetName")
    @property
    def asset_name(self) -> Optional[str]:
        """Gets the assetName property"""
        return self.properties.get("assetName", None)

    @odata(name="assetPublisher")
    @property
    def asset_publisher(self) -> Optional[str]:
        """Gets the assetPublisher property"""
        return self.properties.get("assetPublisher", None)

    @odata(name="assetVersion")
    @property
    def asset_version(self) -> Optional[str]:
        """Gets the assetVersion property"""
        return self.properties.get("assetVersion", None)

    @odata(name="detectionModelId")
    @property
    def detection_model_id(self) -> Optional[str]:
        """Gets the detectionModelId property"""
        return self.properties.get("detectionModelId", None)

    @odata(name="deviceImpactedCount")
    @property
    def device_impacted_count(self) -> Optional[int]:
        """Gets the deviceImpactedCount property"""
        return self.properties.get("deviceImpactedCount", None)

    @odata(name="issueId")
    @property
    def issue_id(self) -> Optional[str]:
        """Gets the issueId property"""
        return self.properties.get("issueId", None)

    @odata(name="severity")
    @property
    def severity(self) -> Optional[UserExperienceAnalyticsAnomalySeverity]:
        """Gets the severity property"""
        return self.properties.get("severity", None)

    @odata(name="state")
    @property
    def state(self) -> Optional[UserExperienceAnalyticsAnomalyState]:
        """Gets the state property"""
        return self.properties.get("state", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAnomaly"
