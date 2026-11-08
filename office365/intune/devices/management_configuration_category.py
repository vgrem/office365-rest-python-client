from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management_configuration_platforms import DeviceManagementConfigurationPlatforms
from office365.intune.devices.management_configuration_setting_usage import DeviceManagementConfigurationSettingUsage
from office365.intune.devices.management_configuration_technologies import DeviceManagementConfigurationTechnologies
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementConfigurationCategory(Entity):
    @odata(name="categoryDescription")
    @property
    def category_description(self) -> Optional[str]:
        """Gets the categoryDescription property"""
        return self.properties.get("categoryDescription", None)

    @odata(name="childCategoryIds")
    @property
    def child_category_ids(self) -> StringCollection:
        """Gets the childCategoryIds property"""
        return self.properties.get("childCategoryIds", StringCollection())

    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="helpText")
    @property
    def help_text(self) -> Optional[str]:
        """Gets the helpText property"""
        return self.properties.get("helpText", None)

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="parentCategoryId")
    @property
    def parent_category_id(self) -> Optional[str]:
        """Gets the parentCategoryId property"""
        return self.properties.get("parentCategoryId", None)

    @odata(name="platforms")
    @property
    def platforms(self) -> Optional[DeviceManagementConfigurationPlatforms]:
        """Gets the platforms property"""
        return self.properties.get("platforms", None)

    @odata(name="rootCategoryId")
    @property
    def root_category_id(self) -> Optional[str]:
        """Gets the rootCategoryId property"""
        return self.properties.get("rootCategoryId", None)

    @odata(name="settingUsage")
    @property
    def setting_usage(self) -> Optional[DeviceManagementConfigurationSettingUsage]:
        """Gets the settingUsage property"""
        return self.properties.get("settingUsage", None)

    @odata(name="technologies")
    @property
    def technologies(self) -> Optional[DeviceManagementConfigurationTechnologies]:
        """Gets the technologies property"""
        return self.properties.get("technologies", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationCategory"
