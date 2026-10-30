from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class UserExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric(Entity):
    @odata(name="osCheckFailedPercentage")
    @property
    def os_check_failed_percentage(self) -> Optional[float]:
        """Gets the osCheckFailedPercentage property"""
        return self.properties.get("osCheckFailedPercentage", None)

    @odata(name="processor64BitCheckFailedPercentage")
    @property
    def processor64_bit_check_failed_percentage(self) -> Optional[float]:
        """Gets the processor64BitCheckFailedPercentage property"""
        return self.properties.get("processor64BitCheckFailedPercentage", None)

    @odata(name="processorCoreCountCheckFailedPercentage")
    @property
    def processor_core_count_check_failed_percentage(self) -> Optional[float]:
        """Gets the processorCoreCountCheckFailedPercentage property"""
        return self.properties.get("processorCoreCountCheckFailedPercentage", None)

    @odata(name="processorFamilyCheckFailedPercentage")
    @property
    def processor_family_check_failed_percentage(self) -> Optional[float]:
        """Gets the processorFamilyCheckFailedPercentage property"""
        return self.properties.get("processorFamilyCheckFailedPercentage", None)

    @odata(name="processorSpeedCheckFailedPercentage")
    @property
    def processor_speed_check_failed_percentage(self) -> Optional[float]:
        """Gets the processorSpeedCheckFailedPercentage property"""
        return self.properties.get("processorSpeedCheckFailedPercentage", None)

    @odata(name="ramCheckFailedPercentage")
    @property
    def ram_check_failed_percentage(self) -> Optional[float]:
        """Gets the ramCheckFailedPercentage property"""
        return self.properties.get("ramCheckFailedPercentage", None)

    @odata(name="secureBootCheckFailedPercentage")
    @property
    def secure_boot_check_failed_percentage(self) -> Optional[float]:
        """Gets the secureBootCheckFailedPercentage property"""
        return self.properties.get("secureBootCheckFailedPercentage", None)

    @odata(name="storageCheckFailedPercentage")
    @property
    def storage_check_failed_percentage(self) -> Optional[float]:
        """Gets the storageCheckFailedPercentage property"""
        return self.properties.get("storageCheckFailedPercentage", None)

    @odata(name="totalDeviceCount")
    @property
    def total_device_count(self) -> Optional[int]:
        """Gets the totalDeviceCount property"""
        return self.properties.get("totalDeviceCount", None)

    @odata(name="tpmCheckFailedPercentage")
    @property
    def tpm_check_failed_percentage(self) -> Optional[float]:
        """Gets the tpmCheckFailedPercentage property"""
        return self.properties.get("tpmCheckFailedPercentage", None)

    @odata(name="upgradeEligibleDeviceCount")
    @property
    def upgrade_eligible_device_count(self) -> Optional[int]:
        """Gets the upgradeEligibleDeviceCount property"""
        return self.properties.get("upgradeEligibleDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsWorkFromAnywhereHardwareReadinessMetric"
