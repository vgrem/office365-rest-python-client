from __future__ import annotations

from typing import Optional

from office365.common.group_policy_setting_scope import GroupPolicySettingScope
from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UnsupportedGroupPolicyExtension(Entity):
    @odata(name="extensionType")
    @property
    def extension_type(self) -> Optional[str]:
        """Gets the extensionType property"""
        return self.properties.get("extensionType", None)

    @odata(name="namespaceUrl")
    @property
    def namespace_url(self) -> Optional[str]:
        """Gets the namespaceUrl property"""
        return self.properties.get("namespaceUrl", None)

    @odata(name="nodeName")
    @property
    def node_name(self) -> Optional[str]:
        """Gets the nodeName property"""
        return self.properties.get("nodeName", None)

    @odata(name="settingScope")
    @property
    def setting_scope(self) -> Optional[GroupPolicySettingScope]:
        """Gets the settingScope property"""
        return self.properties.get("settingScope", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnsupportedGroupPolicyExtension"
