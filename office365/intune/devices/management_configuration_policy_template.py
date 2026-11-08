from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management_configuration_platforms import DeviceManagementConfigurationPlatforms
from office365.intune.devices.management_configuration_technologies import DeviceManagementConfigurationTechnologies
from office365.intune.devices.management_configuration_template_family import DeviceManagementConfigurationTemplateFamily
from office365.intune.devices.management_template_lifecycle_state import DeviceManagementTemplateLifecycleState
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_configuration_setting_template import (
        DeviceManagementConfigurationSettingTemplate,
    )


@version("beta")
class DeviceManagementConfigurationPolicyTemplate(Entity):
    @odata(name="allowUnmanagedSettings")
    @property
    def allow_unmanaged_settings(self) -> Optional[bool]:
        """Gets the allowUnmanagedSettings property"""
        return self.properties.get("allowUnmanagedSettings", None)

    @odata(name="baseId")
    @property
    def base_id(self) -> Optional[str]:
        """Gets the baseId property"""
        return self.properties.get("baseId", None)

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="disableEntraGroupPolicyAssignment")
    @property
    def disable_entra_group_policy_assignment(self) -> Optional[bool]:
        """Gets the disableEntraGroupPolicyAssignment property"""
        return self.properties.get("disableEntraGroupPolicyAssignment", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="displayVersion")
    @property
    def display_version(self) -> Optional[str]:
        """Gets the displayVersion property"""
        return self.properties.get("displayVersion", None)

    @odata(name="lifecycleState")
    @property
    def lifecycle_state(self) -> Optional[DeviceManagementTemplateLifecycleState]:
        """Gets the lifecycleState property"""
        return self.properties.get("lifecycleState", None)

    @odata(name="platforms")
    @property
    def platforms(self) -> Optional[DeviceManagementConfigurationPlatforms]:
        """Gets the platforms property"""
        return self.properties.get("platforms", None)

    @odata(name="settingTemplateCount", readonly=True)
    @property
    def setting_template_count(self) -> Optional[int]:
        """Gets the settingTemplateCount property"""
        return self.properties.get("settingTemplateCount", None)

    @odata(name="technologies")
    @property
    def technologies(self) -> Optional[DeviceManagementConfigurationTechnologies]:
        """Gets the technologies property"""
        return self.properties.get("technologies", None)

    @odata(name="templateFamily")
    @property
    def template_family(self) -> Optional[DeviceManagementConfigurationTemplateFamily]:
        """Gets the templateFamily property"""
        return self.properties.get("templateFamily", None)

    @odata(name="version", readonly=True)
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="settingTemplates", navigation=True)
    @property
    def setting_templates(self) -> EntityCollection[DeviceManagementConfigurationSettingTemplate]:
        """Gets the settingTemplates property"""
        from office365.intune.devices.management_configuration_setting_template import (
            DeviceManagementConfigurationSettingTemplate,
        )

        return self.properties.get(
            "settingTemplates",
            EntityCollection[DeviceManagementConfigurationSettingTemplate](
                self.context,
                DeviceManagementConfigurationSettingTemplate,
                ResourcePath("settingTemplates", self.resource_path),
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationPolicyTemplate"
