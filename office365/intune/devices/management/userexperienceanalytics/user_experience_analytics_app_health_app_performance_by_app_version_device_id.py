from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId(Entity):
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

    @odata(name="deviceDisplayName")
    @property
    def device_display_name(self) -> Optional[str]:
        """Gets the deviceDisplayName property"""
        return self.properties.get("deviceDisplayName", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="processedDateTime")
    @property
    def processed_date_time(self) -> Optional[datetime]:
        """Gets the processedDateTime property"""
        return self.properties.get("processedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAppHealthAppPerformanceByAppVersionDeviceId"
