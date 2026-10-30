from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.userexperienceanalytics.disktype import (
        DiskType,
    )
    from office365.intune.devices.management.userexperienceanalytics.healthstate import (
        UserExperienceAnalyticsHealthState,
    )


class UserExperienceAnalyticsDevicePerformance(Entity):
    @odata(name="averageBlueScreens")
    @property
    def average_blue_screens(self) -> Optional[float]:
        """Gets the averageBlueScreens property"""
        return self.properties.get("averageBlueScreens", None)

    @odata(name="averageRestarts")
    @property
    def average_restarts(self) -> Optional[float]:
        """Gets the averageRestarts property"""
        return self.properties.get("averageRestarts", None)

    @odata(name="blueScreenCount")
    @property
    def blue_screen_count(self) -> Optional[int]:
        """Gets the blueScreenCount property"""
        return self.properties.get("blueScreenCount", None)

    @odata(name="bootScore")
    @property
    def boot_score(self) -> Optional[int]:
        """Gets the bootScore property"""
        return self.properties.get("bootScore", None)

    @odata(name="coreBootTimeInMs")
    @property
    def core_boot_time_in_ms(self) -> Optional[int]:
        """Gets the coreBootTimeInMs property"""
        return self.properties.get("coreBootTimeInMs", None)

    @odata(name="coreLoginTimeInMs")
    @property
    def core_login_time_in_ms(self) -> Optional[int]:
        """Gets the coreLoginTimeInMs property"""
        return self.properties.get("coreLoginTimeInMs", None)

    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="diskType")
    @property
    def disk_type(self) -> DiskType:
        """Gets the diskType property"""
        from office365.intune.devices.management.userexperienceanalytics.disktype import (
            DiskType,
        )

        return self.properties.get("diskType", DiskType.unknown)

    @odata(name="groupPolicyBootTimeInMs")
    @property
    def group_policy_boot_time_in_ms(self) -> Optional[int]:
        """Gets the groupPolicyBootTimeInMs property"""
        return self.properties.get("groupPolicyBootTimeInMs", None)

    @odata(name="groupPolicyLoginTimeInMs")
    @property
    def group_policy_login_time_in_ms(self) -> Optional[int]:
        """Gets the groupPolicyLoginTimeInMs property"""
        return self.properties.get("groupPolicyLoginTimeInMs", None)

    @odata(name="healthStatus")
    @property
    def health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the healthStatus property"""
        from office365.intune.devices.management.userexperienceanalytics.healthstate import (
            UserExperienceAnalyticsHealthState,
        )

        return self.properties.get("healthStatus", UserExperienceAnalyticsHealthState.unknown)

    @odata(name="loginScore")
    @property
    def login_score(self) -> Optional[int]:
        """Gets the loginScore property"""
        return self.properties.get("loginScore", None)

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

    @odata(name="modelStartupPerformanceScore")
    @property
    def model_startup_performance_score(self) -> Optional[float]:
        """Gets the modelStartupPerformanceScore property"""
        return self.properties.get("modelStartupPerformanceScore", None)

    @odata(name="operatingSystemVersion")
    @property
    def operating_system_version(self) -> Optional[str]:
        """Gets the operatingSystemVersion property"""
        return self.properties.get("operatingSystemVersion", None)

    @odata(name="responsiveDesktopTimeInMs")
    @property
    def responsive_desktop_time_in_ms(self) -> Optional[int]:
        """Gets the responsiveDesktopTimeInMs property"""
        return self.properties.get("responsiveDesktopTimeInMs", None)

    @odata(name="restartCount")
    @property
    def restart_count(self) -> Optional[int]:
        """Gets the restartCount property"""
        return self.properties.get("restartCount", None)

    @odata(name="startupPerformanceScore")
    @property
    def startup_performance_score(self) -> Optional[float]:
        """Gets the startupPerformanceScore property"""
        return self.properties.get("startupPerformanceScore", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDevicePerformance"
