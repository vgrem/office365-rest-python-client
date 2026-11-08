from __future__ import annotations

from office365.runtime.client_value import ClientValue


class DeviceManagementConfigurationSettingInstanceTemplate(ClientValue):
    isRequired: bool | None = None
    settingDefinitionId: str | None = None
    settingInstanceTemplateId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingInstanceTemplate"
