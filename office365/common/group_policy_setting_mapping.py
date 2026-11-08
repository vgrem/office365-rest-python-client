from __future__ import annotations

from typing import Optional

from office365.common.group_policy_setting_scope import GroupPolicySettingScope
from office365.common.group_policy_setting_type import GroupPolicySettingType
from office365.common.mdm_supported_state import MdmSupportedState
from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version


@version("beta")
class GroupPolicySettingMapping(Entity):
    @odata(name="admxSettingDefinitionId")
    @property
    def admx_setting_definition_id(self) -> Optional[str]:
        """Gets the admxSettingDefinitionId property"""
        return self.properties.get("admxSettingDefinitionId", None)

    @odata(name="childIdList")
    @property
    def child_id_list(self) -> StringCollection:
        """Gets the childIdList property"""
        return self.properties.get("childIdList", StringCollection())

    @odata(name="intuneSettingDefinitionId")
    @property
    def intune_setting_definition_id(self) -> Optional[str]:
        """Gets the intuneSettingDefinitionId property"""
        return self.properties.get("intuneSettingDefinitionId", None)

    @odata(name="intuneSettingUriList")
    @property
    def intune_setting_uri_list(self) -> StringCollection:
        """Gets the intuneSettingUriList property"""
        return self.properties.get("intuneSettingUriList", StringCollection())

    @odata(name="isMdmSupported")
    @property
    def is_mdm_supported(self) -> Optional[bool]:
        """Gets the isMdmSupported property"""
        return self.properties.get("isMdmSupported", None)

    @odata(name="mdmCspName")
    @property
    def mdm_csp_name(self) -> Optional[str]:
        """Gets the mdmCspName property"""
        return self.properties.get("mdmCspName", None)

    @odata(name="mdmMinimumOSVersion")
    @property
    def mdm_minimum_os_version(self) -> Optional[int]:
        """Gets the mdmMinimumOSVersion property"""
        return self.properties.get("mdmMinimumOSVersion", None)

    @odata(name="mdmSettingUri")
    @property
    def mdm_setting_uri(self) -> Optional[str]:
        """Gets the mdmSettingUri property"""
        return self.properties.get("mdmSettingUri", None)

    @odata(name="mdmSupportedState")
    @property
    def mdm_supported_state(self) -> Optional[MdmSupportedState]:
        """Gets the mdmSupportedState property"""
        return self.properties.get("mdmSupportedState", None)

    @odata(name="parentId")
    @property
    def parent_id(self) -> Optional[str]:
        """Gets the parentId property"""
        return self.properties.get("parentId", None)

    @odata(name="settingCategory")
    @property
    def setting_category(self) -> Optional[str]:
        """Gets the settingCategory property"""
        return self.properties.get("settingCategory", None)

    @odata(name="settingDisplayName")
    @property
    def setting_display_name(self) -> Optional[str]:
        """Gets the settingDisplayName property"""
        return self.properties.get("settingDisplayName", None)

    @odata(name="settingDisplayValue")
    @property
    def setting_display_value(self) -> Optional[str]:
        """Gets the settingDisplayValue property"""
        return self.properties.get("settingDisplayValue", None)

    @odata(name="settingDisplayValueType")
    @property
    def setting_display_value_type(self) -> Optional[str]:
        """Gets the settingDisplayValueType property"""
        return self.properties.get("settingDisplayValueType", None)

    @odata(name="settingName")
    @property
    def setting_name(self) -> Optional[str]:
        """Gets the settingName property"""
        return self.properties.get("settingName", None)

    @odata(name="settingScope")
    @property
    def setting_scope(self) -> Optional[GroupPolicySettingScope]:
        """Gets the settingScope property"""
        return self.properties.get("settingScope", None)

    @odata(name="settingType")
    @property
    def setting_type(self) -> Optional[GroupPolicySettingType]:
        """Gets the settingType property"""
        return self.properties.get("settingType", None)

    @odata(name="settingValue")
    @property
    def setting_value(self) -> Optional[str]:
        """Gets the settingValue property"""
        return self.properties.get("settingValue", None)

    @odata(name="settingValueDisplayUnits")
    @property
    def setting_value_display_units(self) -> Optional[str]:
        """Gets the settingValueDisplayUnits property"""
        return self.properties.get("settingValueDisplayUnits", None)

    @odata(name="settingValueType")
    @property
    def setting_value_type(self) -> Optional[str]:
        """Gets the settingValueType property"""
        return self.properties.get("settingValueType", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupPolicySettingMapping"
