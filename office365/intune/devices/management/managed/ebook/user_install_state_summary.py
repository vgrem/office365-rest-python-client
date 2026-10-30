from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.intune.devices.install_state import DeviceInstallState


class UserInstallStateSummary(Entity):
    @odata(name="failedDeviceCount")
    @property
    def failed_device_count(self) -> Optional[int]:
        """Gets the failedDeviceCount property"""
        return self.properties.get("failedDeviceCount", None)

    @odata(name="installedDeviceCount")
    @property
    def installed_device_count(self) -> Optional[int]:
        """Gets the installedDeviceCount property"""
        return self.properties.get("installedDeviceCount", None)

    @odata(name="notInstalledDeviceCount")
    @property
    def not_installed_device_count(self) -> Optional[int]:
        """Gets the notInstalledDeviceCount property"""
        return self.properties.get("notInstalledDeviceCount", None)

    @odata(name="userName")
    @property
    def user_name(self) -> Optional[str]:
        """Gets the userName property"""
        return self.properties.get("userName", None)

    @odata(name="deviceStates", navigation=True)
    @property
    def device_states(self) -> EntityCollection[DeviceInstallState]:
        """Gets the deviceStates property"""
        from office365.intune.devices.install_state import DeviceInstallState

        return self.properties.get(
            "deviceStates",
            EntityCollection[DeviceInstallState](
                self.context, DeviceInstallState, ResourcePath("deviceStates", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserInstallStateSummary"
