from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.healthstate import UserExperienceAnalyticsHealthState
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsWorkFromAnywhereModelPerformance(Entity):
    @odata(name="cloudIdentityScore")
    @property
    def cloud_identity_score(self) -> Optional[float]:
        """Gets the cloudIdentityScore property"""
        return self.properties.get("cloudIdentityScore", None)

    @odata(name="cloudManagementScore")
    @property
    def cloud_management_score(self) -> Optional[float]:
        """Gets the cloudManagementScore property"""
        return self.properties.get("cloudManagementScore", None)

    @odata(name="cloudProvisioningScore")
    @property
    def cloud_provisioning_score(self) -> Optional[float]:
        """Gets the cloudProvisioningScore property"""
        return self.properties.get("cloudProvisioningScore", None)

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

    @odata(name="model")
    @property
    def model(self) -> Optional[str]:
        """Gets the model property"""
        return self.properties.get("model", None)

    @odata(name="modelDeviceCount")
    @property
    def model_device_count(self) -> Optional[int]:
        """Gets the modelDeviceCount property"""
        return self.properties.get("modelDeviceCount", None)

    @odata(name="windowsScore")
    @property
    def windows_score(self) -> Optional[float]:
        """Gets the windowsScore property"""
        return self.properties.get("windowsScore", None)

    @odata(name="workFromAnywhereScore")
    @property
    def work_from_anywhere_score(self) -> Optional[float]:
        """Gets the workFromAnywhereScore property"""
        return self.properties.get("workFromAnywhereScore", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsWorkFromAnywhereModelPerformance"
