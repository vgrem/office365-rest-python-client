from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion(Entity):
    @odata(name="activeDeviceCount")
    @property
    def active_device_count(self) -> Optional[int]:
        """Gets the activeDeviceCount property"""
        return self.properties.get("activeDeviceCount", None)

    @odata(name="appCrashCount")
    @property
    def app_crash_count(self) -> Optional[int]:
        """Gets the appCrashCount property"""
        return self.properties.get("appCrashCount", None)

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

    @odata(name="appUsageDuration")
    @property
    def app_usage_duration(self) -> Optional[int]:
        """Gets the appUsageDuration property"""
        return self.properties.get("appUsageDuration", None)

    @odata(name="meanTimeToFailureInMinutes")
    @property
    def mean_time_to_failure_in_minutes(self) -> Optional[int]:
        """Gets the meanTimeToFailureInMinutes property"""
        return self.properties.get("meanTimeToFailureInMinutes", None)

    @odata(name="osBuildNumber")
    @property
    def os_build_number(self) -> Optional[str]:
        """Gets the osBuildNumber property"""
        return self.properties.get("osBuildNumber", None)

    @odata(name="osVersion")
    @property
    def os_version(self) -> Optional[str]:
        """Gets the osVersion property"""
        return self.properties.get("osVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAppHealthAppPerformanceByOSVersion"
