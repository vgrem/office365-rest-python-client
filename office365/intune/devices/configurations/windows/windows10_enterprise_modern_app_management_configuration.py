from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Windows10EnterpriseModernAppManagementConfiguration(Entity):
    @odata(name="uninstallBuiltInApps")
    @property
    def uninstall_built_in_apps(self) -> Optional[bool]:
        """Gets the uninstallBuiltInApps property"""
        return self.properties.get("uninstallBuiltInApps", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10EnterpriseModernAppManagementConfiguration"
