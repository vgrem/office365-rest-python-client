from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.common.run_state import RunState
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.device import ManagedDevice


@version("beta")
class DeviceManagementScriptDeviceState(Entity):
    @odata(name="errorCode")
    @property
    def error_code(self) -> Optional[int]:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", None)

    @odata(name="errorDescription")
    @property
    def error_description(self) -> Optional[str]:
        """Gets the errorDescription property"""
        return self.properties.get("errorDescription", None)

    @odata(name="lastStateUpdateDateTime")
    @property
    def last_state_update_date_time(self) -> Optional[datetime]:
        """Gets the lastStateUpdateDateTime property"""
        return self.properties.get("lastStateUpdateDateTime", None)

    @odata(name="resultMessage")
    @property
    def result_message(self) -> Optional[str]:
        """Gets the resultMessage property"""
        return self.properties.get("resultMessage", None)

    @odata(name="runState")
    @property
    def run_state(self) -> Optional[RunState]:
        """Gets the runState property"""
        return self.properties.get("runState", None)

    @odata(name="managedDevice", navigation=True)
    @property
    def managed_device(self) -> ManagedDevice:
        """Gets the managedDevice property"""
        from office365.intune.devices.management.managed.device import ManagedDevice

        return self.properties.get(
            "managedDevice", ManagedDevice(self.context, ResourcePath("managedDevice", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceManagementScriptDeviceState"
