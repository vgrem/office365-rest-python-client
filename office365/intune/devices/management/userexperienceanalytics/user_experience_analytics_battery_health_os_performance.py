from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.healthstate import UserExperienceAnalyticsHealthState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthOsPerformance(Entity):
    @odata(name="activeDevices")
    @property
    def active_devices(self) -> Optional[int]:
        """Gets the activeDevices property"""
        return self.properties.get("activeDevices", None)

    @odata(name="averageBatteryAgeInDays")
    @property
    def average_battery_age_in_days(self) -> Optional[int]:
        """Gets the averageBatteryAgeInDays property"""
        return self.properties.get("averageBatteryAgeInDays", None)

    @odata(name="averageEstimatedRuntimeInMinutes")
    @property
    def average_estimated_runtime_in_minutes(self) -> Optional[int]:
        """Gets the averageEstimatedRuntimeInMinutes property"""
        return self.properties.get("averageEstimatedRuntimeInMinutes", None)

    @odata(name="averageMaxCapacityPercentage")
    @property
    def average_max_capacity_percentage(self) -> Optional[int]:
        """Gets the averageMaxCapacityPercentage property"""
        return self.properties.get("averageMaxCapacityPercentage", None)

    @odata(name="meanFullBatteryDrainCount")
    @property
    def mean_full_battery_drain_count(self) -> Optional[int]:
        """Gets the meanFullBatteryDrainCount property"""
        return self.properties.get("meanFullBatteryDrainCount", None)

    @odata(name="medianEstimatedRuntimeInMinutes")
    @property
    def median_estimated_runtime_in_minutes(self) -> Optional[int]:
        """Gets the medianEstimatedRuntimeInMinutes property"""
        return self.properties.get("medianEstimatedRuntimeInMinutes", None)

    @odata(name="medianFullBatteryDrainCount")
    @property
    def median_full_battery_drain_count(self) -> Optional[int]:
        """Gets the medianFullBatteryDrainCount property"""
        return self.properties.get("medianFullBatteryDrainCount", None)

    @odata(name="medianMaxCapacityPercentage")
    @property
    def median_max_capacity_percentage(self) -> Optional[int]:
        """Gets the medianMaxCapacityPercentage property"""
        return self.properties.get("medianMaxCapacityPercentage", None)

    @odata(name="osBatteryHealthScore")
    @property
    def os_battery_health_score(self) -> Optional[int]:
        """Gets the osBatteryHealthScore property"""
        return self.properties.get("osBatteryHealthScore", None)

    @odata(name="osBuildNumber")
    @property
    def os_build_number(self) -> Optional[str]:
        """Gets the osBuildNumber property"""
        return self.properties.get("osBuildNumber", None)

    @odata(name="osHealthStatus")
    @property
    def os_health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the osHealthStatus property"""
        return self.properties.get("osHealthStatus", UserExperienceAnalyticsHealthState.unknown)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthOsPerformance"
