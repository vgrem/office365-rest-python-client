from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management_configuration_control_type import DeviceManagementConfigurationControlType
from office365.intune.devices.management_configuration_referred_setting_information import (
    DeviceManagementConfigurationReferredSettingInformation,
)
from office365.intune.devices.management_configuration_setting_access_types import (
    DeviceManagementConfigurationSettingAccessTypes,
)
from office365.intune.devices.management_configuration_setting_applicability import (
    DeviceManagementConfigurationSettingApplicability,
)
from office365.intune.devices.management_configuration_setting_occurrence import (
    DeviceManagementConfigurationSettingOccurrence,
)
from office365.intune.devices.management_configuration_setting_risk_level import (
    DeviceManagementConfigurationSettingRiskLevel,
)
from office365.intune.devices.management_configuration_setting_usage import DeviceManagementConfigurationSettingUsage
from office365.intune.devices.management_configuration_setting_visibility import (
    DeviceManagementConfigurationSettingVisibility,
)
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceManagementConfigurationSettingDefinition(Entity):
    @odata(name="accessTypes")
    @property
    def access_types(self) -> Optional[DeviceManagementConfigurationSettingAccessTypes]:
        """Gets the accessTypes property"""
        return self.properties.get("accessTypes", None)

    @odata(name="applicability")
    @property
    def applicability(self) -> Optional[DeviceManagementConfigurationSettingApplicability]:
        """Gets the applicability property"""
        return self.properties.get("applicability", None)

    @odata(name="baseUri")
    @property
    def base_uri(self) -> Optional[str]:
        """Gets the baseUri property"""
        return self.properties.get("baseUri", None)

    @odata(name="categoryId")
    @property
    def category_id(self) -> Optional[str]:
        """Gets the categoryId property"""
        return self.properties.get("categoryId", None)

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

    @odata(name="infoUrls")
    @property
    def info_urls(self) -> StringCollection:
        """Gets the infoUrls property"""
        return self.properties.get("infoUrls", StringCollection())

    @odata(name="keywords")
    @property
    def keywords(self) -> StringCollection:
        """Gets the keywords property"""
        return self.properties.get("keywords", StringCollection())

    @odata(name="name")
    @property
    def name(self) -> Optional[str]:
        """Gets the name property"""
        return self.properties.get("name", None)

    @odata(name="occurrence")
    @property
    def occurrence(self) -> Optional[DeviceManagementConfigurationSettingOccurrence]:
        """Gets the occurrence property"""
        return self.properties.get("occurrence", None)

    @odata(name="offsetUri")
    @property
    def offset_uri(self) -> Optional[str]:
        """Gets the offsetUri property"""
        return self.properties.get("offsetUri", None)

    @odata(name="referredSettingInformationList")
    @property
    def referred_setting_information_list(
        self,
    ) -> ClientValueCollection[DeviceManagementConfigurationReferredSettingInformation]:
        """Gets the referredSettingInformationList property"""
        return self.properties.get(
            "referredSettingInformationList",
            ClientValueCollection[DeviceManagementConfigurationReferredSettingInformation](
                DeviceManagementConfigurationReferredSettingInformation
            ),
        )

    @odata(name="riskLevel")
    @property
    def risk_level(self) -> Optional[DeviceManagementConfigurationSettingRiskLevel]:
        """Gets the riskLevel property"""
        return self.properties.get("riskLevel", None)

    @odata(name="rootDefinitionId")
    @property
    def root_definition_id(self) -> Optional[str]:
        """Gets the rootDefinitionId property"""
        return self.properties.get("rootDefinitionId", None)

    @odata(name="settingUsage")
    @property
    def setting_usage(self) -> Optional[DeviceManagementConfigurationSettingUsage]:
        """Gets the settingUsage property"""
        return self.properties.get("settingUsage", None)

    @odata(name="uxBehavior")
    @property
    def ux_behavior(self) -> Optional[DeviceManagementConfigurationControlType]:
        """Gets the uxBehavior property"""
        return self.properties.get("uxBehavior", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="visibility")
    @property
    def visibility(self) -> Optional[DeviceManagementConfigurationSettingVisibility]:
        """Gets the visibility property"""
        return self.properties.get("visibility", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementConfigurationSettingDefinition"
