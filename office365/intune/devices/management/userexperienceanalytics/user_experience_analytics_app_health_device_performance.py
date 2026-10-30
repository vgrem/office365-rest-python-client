from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.userexperienceanalytics.healthstate import (
        UserExperienceAnalyticsHealthState,
    )


class UserExperienceAnalyticsAppHealthDevicePerformance(Entity):
    @odata(name="appCrashCount")
    @property
    def app_crash_count(self) -> Optional[int]:
        """Gets the appCrashCount property"""
        return self.properties.get("appCrashCount", None)

    @odata(name="appHangCount")
    @property
    def app_hang_count(self) -> Optional[int]:
        """Gets the appHangCount property"""
        return self.properties.get("appHangCount", None)

    @odata(name="crashedAppCount")
    @property
    def crashed_app_count(self) -> Optional[int]:
        """Gets the crashedAppCount property"""
        return self.properties.get("crashedAppCount", None)

    @odata(name="deviceAppHealthScore")
    @property
    def device_app_health_score(self) -> Optional[float]:
        """Gets the deviceAppHealthScore property"""
        return self.properties.get("deviceAppHealthScore", None)

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

    @odata(name="deviceManufacturer")
    @property
    def device_manufacturer(self) -> Optional[str]:
        """Gets the deviceManufacturer property"""
        return self.properties.get("deviceManufacturer", None)

    @odata(name="deviceModel")
    @property
    def device_model(self) -> Optional[str]:
        """Gets the deviceModel property"""
        return self.properties.get("deviceModel", None)

    @odata(name="healthStatus")
    @property
    def health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the healthStatus property"""
        from office365.intune.devices.management.userexperienceanalytics.healthstate import (
            UserExperienceAnalyticsHealthState,
        )

        return self.properties.get("healthStatus", UserExperienceAnalyticsHealthState.unknown)

    @odata(name="meanTimeToFailureInMinutes")
    @property
    def mean_time_to_failure_in_minutes(self) -> Optional[int]:
        """Gets the meanTimeToFailureInMinutes property"""
        return self.properties.get("meanTimeToFailureInMinutes", None)

    @odata(name="processedDateTime")
    @property
    def processed_date_time(self) -> Optional[datetime]:
        """Gets the processedDateTime property"""
        return self.properties.get("processedDateTime", datetime.min)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAppHealthDevicePerformance"
