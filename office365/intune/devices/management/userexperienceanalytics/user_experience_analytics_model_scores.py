from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.userexperienceanalytics.healthstate import (
        UserExperienceAnalyticsHealthState,
    )


class UserExperienceAnalyticsModelScores(Entity):
    @odata(name="appReliabilityScore")
    @property
    def app_reliability_score(self) -> Optional[float]:
        """Gets the appReliabilityScore property"""
        return self.properties.get("appReliabilityScore", None)

    @odata(name="batteryHealthScore")
    @property
    def battery_health_score(self) -> Optional[float]:
        """Gets the batteryHealthScore property"""
        return self.properties.get("batteryHealthScore", None)

    @odata(name="endpointAnalyticsScore")
    @property
    def endpoint_analytics_score(self) -> Optional[float]:
        """Gets the endpointAnalyticsScore property"""
        return self.properties.get("endpointAnalyticsScore", None)

    @odata(name="healthStatus")
    @property
    def health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the healthStatus property"""
        from office365.intune.devices.management.userexperienceanalytics.healthstate import (
            UserExperienceAnalyticsHealthState,
        )

        return self.properties.get("healthStatus", UserExperienceAnalyticsHealthState.unknown)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="modelDeviceCount")
    @property
    def model_device_count(self) -> Optional[int]:
        """Gets the modelDeviceCount property"""
        return self.properties.get("modelDeviceCount", None)

    @odata(name="startupPerformanceScore")
    @property
    def startup_performance_score(self) -> Optional[float]:
        """Gets the startupPerformanceScore property"""
        return self.properties.get("startupPerformanceScore", None)

    @odata(name="workFromAnywhereScore")
    @property
    def work_from_anywhere_score(self) -> Optional[float]:
        """Gets the workFromAnywhereScore property"""
        return self.properties.get("workFromAnywhereScore", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsModelScores"
