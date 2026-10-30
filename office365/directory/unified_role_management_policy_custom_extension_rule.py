from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata


class UnifiedRoleManagementPolicyCustomExtensionRule(Entity):
    @odata(name="customAttributes")
    @property
    def custom_attributes(self) -> StringCollection:
        """Gets the customAttributes property"""
        return self.properties.get("customAttributes", StringCollection())

    @odata(name="customExtensionId")
    @property
    def custom_extension_id(self) -> Optional[str]:
        """Gets the customExtensionId property"""
        return self.properties.get("customExtensionId", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleManagementPolicyCustomExtensionRule"
