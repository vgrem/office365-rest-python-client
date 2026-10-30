from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.intune.devices.compliance.policyplatformtype import PolicyPlatformType
from office365.intune.devices.compliance.status import ComplianceStatus
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.configuration_setting_state import (
        DeviceConfigurationSettingState,
    )


class DeviceConfigurationState(Entity):
    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="platformType")
    @property
    def platform_type(self) -> PolicyPlatformType:
        """Gets the platformType property"""
        return self.properties.get("platformType", PolicyPlatformType.android)

    @odata(name="settingCount")
    @property
    def setting_count(self) -> Optional[int]:
        """Gets the settingCount property"""
        return self.properties.get("settingCount", None)

    @odata(name="settingStates")
    @property
    def setting_states(self) -> ClientValueCollection[DeviceConfigurationSettingState]:
        """Gets the settingStates property"""
        from office365.intune.devices.management.configuration_setting_state import (
            DeviceConfigurationSettingState,
        )

        return self.properties.get(
            "settingStates", ClientValueCollection[DeviceConfigurationSettingState](DeviceConfigurationSettingState)
        )

    @odata(name="state")
    @property
    def state(self) -> ComplianceStatus:
        """Gets the state property"""
        return self.properties.get("state", ComplianceStatus.unknown)

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceConfigurationState"
