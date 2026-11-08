from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management_configuration_setting_instance import (
    DeviceManagementConfigurationSettingInstance,
)
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_configuration_setting_definition import (
        DeviceManagementConfigurationSettingDefinition,
    )


@version("beta")
class DeviceManagementConfigurationSetting(Entity):
    @odata(name="settingInstance")
    @property
    def setting_instance(self) -> Optional[DeviceManagementConfigurationSettingInstance]:
        """Gets the settingInstance property"""
        return self.properties.get("settingInstance", None)

    @odata(name="settingDefinitions", navigation=True)
    @property
    def setting_definitions(self) -> EntityCollection[DeviceManagementConfigurationSettingDefinition]:
        """Gets the settingDefinitions property"""
        from office365.intune.devices.management_configuration_setting_definition import (
            DeviceManagementConfigurationSettingDefinition,
        )

        return self.properties.get(
            "settingDefinitions",
            EntityCollection[DeviceManagementConfigurationSettingDefinition](
                self.context,
                DeviceManagementConfigurationSettingDefinition,
                ResourcePath("settingDefinitions", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSetting"
