from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management_script_device_state import DeviceManagementScriptDeviceState


@version("beta")
class DeviceManagementScriptUserState(Entity):
    @odata(name="errorDeviceCount")
    @property
    def error_device_count(self) -> Optional[int]:
        """Gets the errorDeviceCount property"""
        return self.properties.get("errorDeviceCount", None)

    @odata(name="successDeviceCount")
    @property
    def success_device_count(self) -> Optional[int]:
        """Gets the successDeviceCount property"""
        return self.properties.get("successDeviceCount", None)

    @odata(name="userPrincipalName")
    @property
    def user_principal_name(self) -> Optional[str]:
        """Gets the userPrincipalName property"""
        return self.properties.get("userPrincipalName", None)

    @odata(name="deviceRunStates", navigation=True)
    @property
    def device_run_states(self) -> EntityCollection[DeviceManagementScriptDeviceState]:
        """Gets the deviceRunStates property"""
        from office365.intune.devices.management_script_device_state import DeviceManagementScriptDeviceState

        return self.properties.get(
            "deviceRunStates",
            EntityCollection[DeviceManagementScriptDeviceState](
                self.context, DeviceManagementScriptDeviceState, ResourcePath("deviceRunStates", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementScriptUserState"
