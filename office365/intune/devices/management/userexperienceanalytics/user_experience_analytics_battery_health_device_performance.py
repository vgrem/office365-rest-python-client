from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.healthstate import UserExperienceAnalyticsHealthState
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_device_battery_detail import (
    UserExperienceAnalyticsDeviceBatteryDetail,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthDevicePerformance(Entity):
    @odata(name="batteryAgeInDays")
    @property
    def battery_age_in_days(self) -> Optional[int]:
        """Gets the batteryAgeInDays property"""
        return self.properties.get("batteryAgeInDays", None)

    @odata(name="deviceBatteriesDetails")
    @property
    def device_batteries_details(self) -> ClientValueCollection[UserExperienceAnalyticsDeviceBatteryDetail]:
        """Gets the deviceBatteriesDetails property"""
        return self.properties.get(
            "deviceBatteriesDetails",
            ClientValueCollection[UserExperienceAnalyticsDeviceBatteryDetail](
                UserExperienceAnalyticsDeviceBatteryDetail
            ),
        )

    @odata(name="deviceBatteryCount")
    @property
    def device_battery_count(self) -> Optional[int]:
        """Gets the deviceBatteryCount property"""
        return self.properties.get("deviceBatteryCount", None)

    @odata(name="deviceBatteryHealthScore")
    @property
    def device_battery_health_score(self) -> Optional[int]:
        """Gets the deviceBatteryHealthScore property"""
        return self.properties.get("deviceBatteryHealthScore", None)

    @odata(name="deviceBatteryTags")
    @property
    def device_battery_tags(self) -> StringCollection:
        """Gets the deviceBatteryTags property"""
        return self.properties.get("deviceBatteryTags", StringCollection())

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

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

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="estimatedRuntimeInMinutes")
    @property
    def estimated_runtime_in_minutes(self) -> Optional[int]:
        """Gets the estimatedRuntimeInMinutes property"""
        return self.properties.get("estimatedRuntimeInMinutes", None)

    @odata(name="fullBatteryDrainCount")
    @property
    def full_battery_drain_count(self) -> Optional[int]:
        """Gets the fullBatteryDrainCount property"""
        return self.properties.get("fullBatteryDrainCount", None)

    @odata(name="healthStatus")
    @property
    def health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the healthStatus property"""
        return self.properties.get("healthStatus", UserExperienceAnalyticsHealthState.unknown)

    @odata(name="manufacturer")
    @property
    def manufacturer(self) -> Optional[str]:
        """Gets the manufacturer property"""
        return self.properties.get("manufacturer", None)

    @odata(name="maxCapacityPercentage")
    @property
    def max_capacity_percentage(self) -> Optional[int]:
        """Gets the maxCapacityPercentage property"""
        return self.properties.get("maxCapacityPercentage", None)

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthDevicePerformance"
