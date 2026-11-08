from __future__ import annotations

from office365.intune.devices.management_configuration_template_family import DeviceManagementConfigurationTemplateFamily
from office365.runtime.client_value import ClientValue


class DeviceManagementConfigurationPolicyTemplateReference(ClientValue):
    templateDisplayName: str | None = None
    templateDisplayVersion: str | None = None
    templateFamily: DeviceManagementConfigurationTemplateFamily = DeviceManagementConfigurationTemplateFamily.none
    templateId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationPolicyTemplateReference"
