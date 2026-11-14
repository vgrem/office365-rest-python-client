from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_setting_instance import DeviceManagementSettingInstance


@version("beta")
class DeviceManagementIntentSettingCategory(Entity):
    @odata(name="settings", navigation=True)
    @property
    def settings(self) -> EntityCollection[DeviceManagementSettingInstance]:
        """Gets the settings property"""
        from office365.intune.devices.management_setting_instance import DeviceManagementSettingInstance

        return self.properties.get(
            "settings",
            EntityCollection[DeviceManagementSettingInstance](
                self.context, DeviceManagementSettingInstance, ResourcePath("settings", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementIntentSettingCategory"
