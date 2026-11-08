from __future__ import annotations

from office365.intune.devices.management_configuration_device_mode import DeviceManagementConfigurationDeviceMode
from office365.intune.devices.management_configuration_platforms import DeviceManagementConfigurationPlatforms
from office365.intune.devices.management_configuration_technologies import DeviceManagementConfigurationTechnologies
from office365.runtime.client_value import ClientValue


class DeviceManagementConfigurationSettingApplicability(ClientValue):
    description: str | None = None
    deviceMode: DeviceManagementConfigurationDeviceMode = DeviceManagementConfigurationDeviceMode.none
    platform: DeviceManagementConfigurationPlatforms = DeviceManagementConfigurationPlatforms.none
    technologies: DeviceManagementConfigurationTechnologies = DeviceManagementConfigurationTechnologies.none

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingApplicability"
