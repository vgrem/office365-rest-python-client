from __future__ import annotations

from dataclasses import field

from office365.intune.devices.management_configuration_setting_instance_template_reference import (
    DeviceManagementConfigurationSettingInstanceTemplateReference,
)
from office365.runtime.client_value import ClientValue


class DeviceManagementConfigurationSettingInstance(ClientValue):
    settingDefinitionId: str | None = None
    settingInstanceTemplateReference: DeviceManagementConfigurationSettingInstanceTemplateReference = field(
        default_factory=DeviceManagementConfigurationSettingInstanceTemplateReference
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingInstance"
