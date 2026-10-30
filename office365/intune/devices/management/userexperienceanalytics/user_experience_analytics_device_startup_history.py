from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.operatingsystemrestartcategory import (  # noqa: E501
    UserExperienceAnalyticsOperatingSystemRestartCategory,
)
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsDeviceStartupHistory(Entity):
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

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="featureUpdateBootTimeInMs")
    @property
    def feature_update_boot_time_in_ms(self) -> Optional[int]:
        """Gets the featureUpdateBootTimeInMs property"""
        return self.properties.get("featureUpdateBootTimeInMs", None)

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

    @odata(name="isFeatureUpdate")
    @property
    def is_feature_update(self) -> Optional[bool]:
        """Gets the isFeatureUpdate property"""
        return self.properties.get("isFeatureUpdate", None)

    @odata(name="isFirstLogin")
    @property
    def is_first_login(self) -> Optional[bool]:
        """Gets the isFirstLogin property"""
        return self.properties.get("isFirstLogin", None)

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

    @odata(name="restartCategory")
    @property
    def restart_category(self) -> UserExperienceAnalyticsOperatingSystemRestartCategory:
        """Gets the restartCategory property"""
        return self.properties.get("restartCategory", UserExperienceAnalyticsOperatingSystemRestartCategory.unknown)

    @odata(name="restartFaultBucket")
    @property
    def restart_fault_bucket(self) -> Optional[str]:
        """Gets the restartFaultBucket property"""
        return self.properties.get("restartFaultBucket", None)

    @odata(name="restartStopCode")
    @property
    def restart_stop_code(self) -> Optional[str]:
        """Gets the restartStopCode property"""
        return self.properties.get("restartStopCode", None)

    @odata(name="startTime")
    @property
    def start_time(self) -> Optional[datetime]:
        """Gets the startTime property"""
        return self.properties.get("startTime", datetime.min)

    @odata(name="totalBootTimeInMs")
    @property
    def total_boot_time_in_ms(self) -> Optional[int]:
        """Gets the totalBootTimeInMs property"""
        return self.properties.get("totalBootTimeInMs", None)

    @odata(name="totalLoginTimeInMs")
    @property
    def total_login_time_in_ms(self) -> Optional[int]:
        """Gets the totalLoginTimeInMs property"""
        return self.properties.get("totalLoginTimeInMs", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceStartupHistory"
