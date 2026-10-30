from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.intune.devices.configurations.ios.minimum_operating_system import IosMinimumOperatingSystem
from office365.intune.devices.management.mobileapps.ios.ios_device_type import IosDeviceType
from office365.runtime.types.odata_property import odata


class ManagedIOSStoreApp(Entity):
    @odata(name="applicableDeviceType")
    @property
    def applicable_device_type(self) -> IosDeviceType:
        """Gets the applicableDeviceType property"""
        return self.properties.get("applicableDeviceType", IosDeviceType())

    @odata(name="appStoreUrl")
    @property
    def app_store_url(self) -> Optional[str]:
        """Gets the appStoreUrl property"""
        return self.properties.get("appStoreUrl", None)

    @odata(name="bundleId")
    @property
    def bundle_id(self) -> Optional[str]:
        """Gets the bundleId property"""
        return self.properties.get("bundleId", None)

    @odata(name="minimumSupportedOperatingSystem")
    @property
    def minimum_supported_operating_system(self) -> IosMinimumOperatingSystem:
        """Gets the minimumSupportedOperatingSystem property"""
        return self.properties.get("minimumSupportedOperatingSystem", IosMinimumOperatingSystem())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedIOSStoreApp"
