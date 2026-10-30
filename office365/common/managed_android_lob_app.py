from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.configurations.android.minimum_operating_system import AndroidMinimumOperatingSystem
from office365.runtime.types.odata_property import odata


class ManagedAndroidLobApp(Entity):
    @odata(name="minimumSupportedOperatingSystem")
    @property
    def minimum_supported_operating_system(self) -> AndroidMinimumOperatingSystem:
        """Gets the minimumSupportedOperatingSystem property"""
        return self.properties.get("minimumSupportedOperatingSystem", AndroidMinimumOperatingSystem())

    @odata(name="packageId")
    @property
    def package_id(self) -> Optional[str]:
        """Gets the packageId property"""
        return self.properties.get("packageId", None)

    @odata(name="versionCode")
    @property
    def version_code(self) -> Optional[str]:
        """Gets the versionCode property"""
        return self.properties.get("versionCode", None)

    @odata(name="versionName")
    @property
    def version_name(self) -> Optional[str]:
        """Gets the versionName property"""
        return self.properties.get("versionName", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAndroidLobApp"
