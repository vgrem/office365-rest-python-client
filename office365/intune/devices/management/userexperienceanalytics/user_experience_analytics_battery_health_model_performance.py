from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.healthstate import UserExperienceAnalyticsHealthState
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthModelPerformance(Entity):
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

    @odata(name="deviceManufacturerName")
    @property
    def device_manufacturer_name(self) -> Optional[str]:
        """Gets the deviceManufacturerName property"""
        return self.properties.get("deviceManufacturerName", None)

    @odata(name="deviceModelName")
    @property
    def device_model_name(self) -> Optional[str]:
        """Gets the deviceModelName property"""
        return self.properties.get("deviceModelName", None)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

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

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="modelBatteryHealthScore")
    @property
    def model_battery_health_score(self) -> Optional[int]:
        """Gets the modelBatteryHealthScore property"""
        return self.properties.get("modelBatteryHealthScore", None)

    @odata(name="modelHealthStatus")
    @property
    def model_health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the modelHealthStatus property"""
        return self.properties.get("modelHealthStatus", UserExperienceAnalyticsHealthState.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthModelPerformance"
