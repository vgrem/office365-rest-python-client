from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.userexperienceanalytics.disktype import DiskType
from office365.intune.devices.management.userexperienceanalytics.healthstate import UserExperienceAnalyticsHealthState
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_machine_type import (
    UserExperienceAnalyticsMachineType,
)
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsResourcePerformance(Entity):
    @odata(name="averageSpikeTimeScore")
    @property
    def average_spike_time_score(self) -> Optional[int]:
        """Gets the averageSpikeTimeScore property"""
        return self.properties.get("averageSpikeTimeScore", None)

    @odata(name="cpuClockSpeedInMHz")
    @property
    def cpu_clock_speed_in_mhz(self) -> Optional[float]:
        """Gets the cpuClockSpeedInMHz property"""
        return self.properties.get("cpuClockSpeedInMHz", None)

    @odata(name="cpuDisplayName")
    @property
    def cpu_display_name(self) -> Optional[str]:
        """Gets the cpuDisplayName property"""
        return self.properties.get("cpuDisplayName", None)

    @odata(name="cpuSpikeTimePercentage")
    @property
    def cpu_spike_time_percentage(self) -> Optional[float]:
        """Gets the cpuSpikeTimePercentage property"""
        return self.properties.get("cpuSpikeTimePercentage", None)

    @odata(name="cpuSpikeTimePercentageThreshold")
    @property
    def cpu_spike_time_percentage_threshold(self) -> Optional[float]:
        """Gets the cpuSpikeTimePercentageThreshold property"""
        return self.properties.get("cpuSpikeTimePercentageThreshold", None)

    @odata(name="cpuSpikeTimeScore")
    @property
    def cpu_spike_time_score(self) -> Optional[int]:
        """Gets the cpuSpikeTimeScore property"""
        return self.properties.get("cpuSpikeTimeScore", None)

    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="deviceName")
    @property
    def device_name(self) -> Optional[str]:
        """Gets the deviceName property"""
        return self.properties.get("deviceName", None)

    @odata(name="deviceResourcePerformanceScore")
    @property
    def device_resource_performance_score(self) -> Optional[int]:
        """Gets the deviceResourcePerformanceScore property"""
        return self.properties.get("deviceResourcePerformanceScore", None)

    @odata(name="diskType")
    @property
    def disk_type(self) -> DiskType:
        """Gets the diskType property"""
        return self.properties.get("diskType", DiskType.unknown)

    @odata(name="healthStatus")
    @property
    def health_status(self) -> UserExperienceAnalyticsHealthState:
        """Gets the healthStatus property"""
        return self.properties.get("healthStatus", UserExperienceAnalyticsHealthState.unknown)

    @odata(name="machineType")
    @property
    def machine_type(self) -> Optional[UserExperienceAnalyticsMachineType]:
        """Gets the machineType property"""
        return self.properties.get("machineType", None)

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

    @odata(name="ramSpikeTimePercentage")
    @property
    def ram_spike_time_percentage(self) -> Optional[float]:
        """Gets the ramSpikeTimePercentage property"""
        return self.properties.get("ramSpikeTimePercentage", None)

    @odata(name="ramSpikeTimePercentageThreshold")
    @property
    def ram_spike_time_percentage_threshold(self) -> Optional[float]:
        """Gets the ramSpikeTimePercentageThreshold property"""
        return self.properties.get("ramSpikeTimePercentageThreshold", None)

    @odata(name="ramSpikeTimeScore")
    @property
    def ram_spike_time_score(self) -> Optional[int]:
        """Gets the ramSpikeTimeScore property"""
        return self.properties.get("ramSpikeTimeScore", None)

    @odata(name="totalProcessorCoreCount")
    @property
    def total_processor_core_count(self) -> Optional[int]:
        """Gets the totalProcessorCoreCount property"""
        return self.properties.get("totalProcessorCoreCount", None)

    @odata(name="totalRamInMB")
    @property
    def total_ram_in_mb(self) -> Optional[float]:
        """Gets the totalRamInMB property"""
        return self.properties.get("totalRamInMB", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsResourcePerformance"
