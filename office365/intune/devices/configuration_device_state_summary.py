from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class DeviceConfigurationDeviceStateSummary(Entity):
    @odata(name="compliantDeviceCount")
    @property
    def compliant_device_count(self) -> Optional[int]:
        """Gets the compliantDeviceCount property"""
        return self.properties.get("compliantDeviceCount", None)

    @odata(name="conflictDeviceCount")
    @property
    def conflict_device_count(self) -> Optional[int]:
        """Gets the conflictDeviceCount property"""
        return self.properties.get("conflictDeviceCount", None)

    @odata(name="errorDeviceCount")
    @property
    def error_device_count(self) -> Optional[int]:
        """Gets the errorDeviceCount property"""
        return self.properties.get("errorDeviceCount", None)

    @odata(name="nonCompliantDeviceCount")
    @property
    def non_compliant_device_count(self) -> Optional[int]:
        """Gets the nonCompliantDeviceCount property"""
        return self.properties.get("nonCompliantDeviceCount", None)

    @odata(name="notApplicableDeviceCount")
    @property
    def not_applicable_device_count(self) -> Optional[int]:
        """Gets the notApplicableDeviceCount property"""
        return self.properties.get("notApplicableDeviceCount", None)

    @odata(name="remediatedDeviceCount")
    @property
    def remediated_device_count(self) -> Optional[int]:
        """Gets the remediatedDeviceCount property"""
        return self.properties.get("remediatedDeviceCount", None)

    @odata(name="unknownDeviceCount")
    @property
    def unknown_device_count(self) -> Optional[int]:
        """Gets the unknownDeviceCount property"""
        return self.properties.get("unknownDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceConfigurationDeviceStateSummary"
