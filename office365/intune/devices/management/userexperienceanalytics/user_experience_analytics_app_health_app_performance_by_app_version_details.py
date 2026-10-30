from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails(Entity):
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

    @odata(name="appVersion")
    @property
    def app_version(self) -> Optional[str]:
        """Gets the appVersion property"""
        return self.properties.get("appVersion", None)

    @odata(name="deviceCountWithCrashes")
    @property
    def device_count_with_crashes(self) -> Optional[int]:
        """Gets the deviceCountWithCrashes property"""
        return self.properties.get("deviceCountWithCrashes", None)

    @odata(name="isLatestUsedVersion")
    @property
    def is_latest_used_version(self) -> Optional[bool]:
        """Gets the isLatestUsedVersion property"""
        return self.properties.get("isLatestUsedVersion", None)

    @odata(name="isMostUsedVersion")
    @property
    def is_most_used_version(self) -> Optional[bool]:
        """Gets the isMostUsedVersion property"""
        return self.properties.get("isMostUsedVersion", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDetails"
