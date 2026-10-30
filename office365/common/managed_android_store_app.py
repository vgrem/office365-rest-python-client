from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.configurations.android.minimum_operating_system import AndroidMinimumOperatingSystem
from office365.runtime.types.odata_property import odata


class ManagedAndroidStoreApp(Entity):
    @odata(name="appStoreUrl")
    @property
    def app_store_url(self) -> Optional[str]:
        """Gets the appStoreUrl property"""
        return self.properties.get("appStoreUrl", None)

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

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedAndroidStoreApp"
