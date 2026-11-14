from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.exchange_access_state_summary import DeviceExchangeAccessStateSummary
from office365.intune.devices.management.operating_system_summary import DeviceOperatingSystemSummary
from office365.runtime.types.odata_property import odata


class ManagedDeviceOverview(Entity):
    @odata(name="deviceExchangeAccessStateSummary")
    @property
    def device_exchange_access_state_summary(self) -> DeviceExchangeAccessStateSummary:
        """Gets the deviceExchangeAccessStateSummary property"""
        return self.properties.get("deviceExchangeAccessStateSummary", DeviceExchangeAccessStateSummary())

    @odata(name="deviceOperatingSystemSummary")
    @property
    def device_operating_system_summary(self) -> DeviceOperatingSystemSummary:
        """Gets the deviceOperatingSystemSummary property"""
        return self.properties.get("deviceOperatingSystemSummary", DeviceOperatingSystemSummary())

    @odata(name="dualEnrolledDeviceCount")
    @property
    def dual_enrolled_device_count(self) -> Optional[int]:
        """Gets the dualEnrolledDeviceCount property"""
        return self.properties.get("dualEnrolledDeviceCount", None)

    @odata(name="enrolledDeviceCount")
    @property
    def enrolled_device_count(self) -> Optional[int]:
        """Gets the enrolledDeviceCount property"""
        return self.properties.get("enrolledDeviceCount", None)

    @odata(name="mdmEnrolledCount")
    @property
    def mdm_enrolled_count(self) -> Optional[int]:
        """Gets the mdmEnrolledCount property"""
        return self.properties.get("mdmEnrolledCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedDeviceOverview"
