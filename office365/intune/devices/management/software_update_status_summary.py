from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class SoftwareUpdateStatusSummary(Entity):
    @odata(name="compliantDeviceCount")
    @property
    def compliant_device_count(self) -> Optional[int]:
        """Gets the compliantDeviceCount property"""
        return self.properties.get("compliantDeviceCount", None)

    @odata(name="compliantUserCount")
    @property
    def compliant_user_count(self) -> Optional[int]:
        """Gets the compliantUserCount property"""
        return self.properties.get("compliantUserCount", None)

    @odata(name="conflictDeviceCount")
    @property
    def conflict_device_count(self) -> Optional[int]:
        """Gets the conflictDeviceCount property"""
        return self.properties.get("conflictDeviceCount", None)

    @odata(name="conflictUserCount")
    @property
    def conflict_user_count(self) -> Optional[int]:
        """Gets the conflictUserCount property"""
        return self.properties.get("conflictUserCount", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="errorDeviceCount")
    @property
    def error_device_count(self) -> Optional[int]:
        """Gets the errorDeviceCount property"""
        return self.properties.get("errorDeviceCount", None)

    @odata(name="errorUserCount")
    @property
    def error_user_count(self) -> Optional[int]:
        """Gets the errorUserCount property"""
        return self.properties.get("errorUserCount", None)

    @odata(name="nonCompliantDeviceCount")
    @property
    def non_compliant_device_count(self) -> Optional[int]:
        """Gets the nonCompliantDeviceCount property"""
        return self.properties.get("nonCompliantDeviceCount", None)

    @odata(name="nonCompliantUserCount")
    @property
    def non_compliant_user_count(self) -> Optional[int]:
        """Gets the nonCompliantUserCount property"""
        return self.properties.get("nonCompliantUserCount", None)

    @odata(name="notApplicableDeviceCount")
    @property
    def not_applicable_device_count(self) -> Optional[int]:
        """Gets the notApplicableDeviceCount property"""
        return self.properties.get("notApplicableDeviceCount", None)

    @odata(name="notApplicableUserCount")
    @property
    def not_applicable_user_count(self) -> Optional[int]:
        """Gets the notApplicableUserCount property"""
        return self.properties.get("notApplicableUserCount", None)

    @odata(name="remediatedDeviceCount")
    @property
    def remediated_device_count(self) -> Optional[int]:
        """Gets the remediatedDeviceCount property"""
        return self.properties.get("remediatedDeviceCount", None)

    @odata(name="remediatedUserCount")
    @property
    def remediated_user_count(self) -> Optional[int]:
        """Gets the remediatedUserCount property"""
        return self.properties.get("remediatedUserCount", None)

    @odata(name="unknownDeviceCount")
    @property
    def unknown_device_count(self) -> Optional[int]:
        """Gets the unknownDeviceCount property"""
        return self.properties.get("unknownDeviceCount", None)

    @odata(name="unknownUserCount")
    @property
    def unknown_user_count(self) -> Optional[int]:
        """Gets the unknownUserCount property"""
        return self.properties.get("unknownUserCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.SoftwareUpdateStatusSummary"
