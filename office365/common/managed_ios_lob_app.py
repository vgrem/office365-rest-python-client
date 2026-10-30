from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.configurations.ios.minimum_operating_system import IosMinimumOperatingSystem
    from office365.intune.devices.management.mobileapps.ios.ios_device_type import (
        IosDeviceType,
    )


class ManagedIOSLobApp(Entity):
    @odata(name="applicableDeviceType")
    @property
    def applicable_device_type(self) -> IosDeviceType:
        """Gets the applicableDeviceType property"""
        from office365.intune.devices.management.mobileapps.ios.ios_device_type import (
            IosDeviceType,
        )

        return self.properties.get("applicableDeviceType", IosDeviceType())

    @odata(name="buildNumber")
    @property
    def build_number(self) -> Optional[str]:
        """Gets the buildNumber property"""
        return self.properties.get("buildNumber", None)

    @odata(name="bundleId")
    @property
    def bundle_id(self) -> Optional[str]:
        """Gets the bundleId property"""
        return self.properties.get("bundleId", None)

    @odata(name="expirationDateTime")
    @property
    def expiration_date_time(self) -> Optional[datetime]:
        """Gets the expirationDateTime property"""
        return self.properties.get("expirationDateTime", datetime.min)

    @odata(name="minimumSupportedOperatingSystem")
    @property
    def minimum_supported_operating_system(self) -> IosMinimumOperatingSystem:
        """Gets the minimumSupportedOperatingSystem property"""
        from office365.intune.devices.configurations.ios.minimum_operating_system import (
            IosMinimumOperatingSystem,
        )

        return self.properties.get("minimumSupportedOperatingSystem", IosMinimumOperatingSystem())

    @odata(name="versionNumber")
    @property
    def version_number(self) -> Optional[str]:
        """Gets the versionNumber property"""
        return self.properties.get("versionNumber", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ManagedIOSLobApp"
