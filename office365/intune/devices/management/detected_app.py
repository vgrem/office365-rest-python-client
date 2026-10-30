from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.intune.devices.management.detectedappplatformtype import DetectedAppPlatformType
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.managed import ManagedDevice


class DetectedApp(Entity):
    @odata(name="deviceCount")
    @property
    def device_count(self) -> Optional[int]:
        """Gets the deviceCount property"""
        return self.properties.get("deviceCount", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="platform")
    @property
    def platform(self) -> DetectedAppPlatformType:
        """Gets the platform property"""
        return self.properties.get("platform", DetectedAppPlatformType.unknown)

    @odata(name="publisher")
    @property
    def publisher(self) -> Optional[str]:
        """Gets the publisher property"""
        return self.properties.get("publisher", None)

    @odata(name="sizeInByte")
    @property
    def size_in_byte(self) -> Optional[int]:
        """Gets the sizeInByte property"""
        return self.properties.get("sizeInByte", None)

    @odata(name="version")
    @property
    def version(self) -> Optional[str]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="managedDevices", navigation=True)
    @property
    def managed_devices(self) -> EntityCollection[ManagedDevice]:
        """Gets the managedDevices property"""
        from office365.intune.devices.management.managed.managed import ManagedDevice

        return self.properties.get(
            "managedDevices",
            EntityCollection[ManagedDevice](
                self.context, ManagedDevice, ResourcePath("managedDevices", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DetectedApp"
