from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.userexperienceanalytics.healthstate import (
        UserExperienceAnalyticsHealthState,
    )


class UserExperienceAnalyticsAppHealthDeviceModelPerformance(Entity):
    @odata(name="activeDeviceCount")
    @property
    def active_device_count(self) -> Optional[int]:
        """Gets the activeDeviceCount property"""
        return self.properties.get("activeDeviceCount", None)

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

    @odata(name="modelAppHealthScore")
    @property
    def model_app_health_score(self) -> Optional[float]:
        """Gets the modelAppHealthScore property"""
        return self.properties.get("modelAppHealthScore", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsAppHealthDeviceModelPerformance"
