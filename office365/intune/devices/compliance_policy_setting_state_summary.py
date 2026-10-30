from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.compliance.policyplatformtype import PolicyPlatformType
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.compliance_setting_state import (
        DeviceComplianceSettingState,
    )


class DeviceCompliancePolicySettingStateSummary(Entity):
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

    @odata(name="platformType")
    @property
    def platform_type(self) -> PolicyPlatformType:
        """Gets the platformType property"""
        return self.properties.get("platformType", PolicyPlatformType.android)

    @odata(name="remediatedDeviceCount")
    @property
    def remediated_device_count(self) -> Optional[int]:
        """Gets the remediatedDeviceCount property"""
        return self.properties.get("remediatedDeviceCount", None)

    @odata(name="setting")
    @property
    def setting(self) -> Optional[str]:
        """Gets the setting property"""
        return self.properties.get("setting", None)

    @odata(name="settingName")
    @property
    def setting_name(self) -> Optional[str]:
        """Gets the settingName property"""
        return self.properties.get("settingName", None)

    @odata(name="unknownDeviceCount")
    @property
    def unknown_device_count(self) -> Optional[int]:
        """Gets the unknownDeviceCount property"""
        return self.properties.get("unknownDeviceCount", None)

    @odata(name="deviceComplianceSettingStates", navigation=True)
    @property
    def device_compliance_setting_states(self) -> EntityCollection[DeviceComplianceSettingState]:
        """Gets the deviceComplianceSettingStates property"""
        from office365.intune.devices.compliance_setting_state import (
            DeviceComplianceSettingState,
        )

        return self.properties.get(
            "deviceComplianceSettingStates",
            EntityCollection[DeviceComplianceSettingState](
                self.context,
                DeviceComplianceSettingState,
                ResourcePath("deviceComplianceSettingStates", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceCompliancePolicySettingStateSummary"
