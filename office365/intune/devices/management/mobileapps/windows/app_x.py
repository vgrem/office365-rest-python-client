from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.configurations.windows.minimum_operating_system import (
        WindowsMinimumOperatingSystem,
    )
    from office365.intune.devices.management.mobileapps.windows.architecture import (
        WindowsArchitecture,
    )


class WindowsAppX(Entity):
    @odata(name="applicableArchitectures")
    @property
    def applicable_architectures(self) -> WindowsArchitecture:
        """Gets the applicableArchitectures property"""
        from office365.intune.devices.management.mobileapps.windows.architecture import (
            WindowsArchitecture,
        )

        return self.properties.get("applicableArchitectures", WindowsArchitecture.none)

    @odata(name="identityName")
    @property
    def identity_name(self) -> Optional[str]:
        """Gets the identityName property"""
        return self.properties.get("identityName", None)

    @odata(name="identityPublisherHash")
    @property
    def identity_publisher_hash(self) -> Optional[str]:
        """Gets the identityPublisherHash property"""
        return self.properties.get("identityPublisherHash", None)

    @odata(name="identityResourceIdentifier")
    @property
    def identity_resource_identifier(self) -> Optional[str]:
        """Gets the identityResourceIdentifier property"""
        return self.properties.get("identityResourceIdentifier", None)

    @odata(name="identityVersion")
    @property
    def identity_version(self) -> Optional[str]:
        """Gets the identityVersion property"""
        return self.properties.get("identityVersion", None)

    @odata(name="isBundle")
    @property
    def is_bundle(self) -> Optional[bool]:
        """Gets the isBundle property"""
        return self.properties.get("isBundle", None)

    @odata(name="minimumSupportedOperatingSystem")
    @property
    def minimum_supported_operating_system(self) -> WindowsMinimumOperatingSystem:
        """Gets the minimumSupportedOperatingSystem property"""
        from office365.intune.devices.configurations.windows.minimum_operating_system import (
            WindowsMinimumOperatingSystem,
        )

        return self.properties.get("minimumSupportedOperatingSystem", WindowsMinimumOperatingSystem())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsAppX"
