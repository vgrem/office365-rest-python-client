from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsBatteryHealthAppImpact(Entity):
    @odata(name="activeDevices")
    @property
    def active_devices(self) -> Optional[int]:
        """Gets the activeDevices property"""
        return self.properties.get("activeDevices", None)

    @odata(name="appDisplayName")
    @property
    def app_display_name(self) -> Optional[str]:
        """Gets the appDisplayName property"""
        return self.properties.get("appDisplayName", None)

    @odata(name="appName")
    @property
    def app_name(self) -> Optional[str]:
        """Gets the appName property"""
        return self.properties.get("appName", None)

    @odata(name="appPublisher")
    @property
    def app_publisher(self) -> Optional[str]:
        """Gets the appPublisher property"""
        return self.properties.get("appPublisher", None)

    @odata(name="batteryUsagePercentage")
    @property
    def battery_usage_percentage(self) -> Optional[float]:
        """Gets the batteryUsagePercentage property"""
        return self.properties.get("batteryUsagePercentage", None)

    @odata(name="isForegroundApp")
    @property
    def is_foreground_app(self) -> Optional[bool]:
        """Gets the isForegroundApp property"""
        return self.properties.get("isForegroundApp", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsBatteryHealthAppImpact"
