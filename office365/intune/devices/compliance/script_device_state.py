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
class DeviceComplianceScriptDeviceState(Entity):
    @odata(name="detectionState")
    @property
    def detection_state(self) -> Optional[RunState]:
        """Gets the detectionState property"""
        return self.properties.get("detectionState", None)

    @odata(name="expectedStateUpdateDateTime")
    @property
    def expected_state_update_date_time(self) -> Optional[datetime]:
        """Gets the expectedStateUpdateDateTime property"""
        return self.properties.get("expectedStateUpdateDateTime", None)

    @odata(name="lastStateUpdateDateTime")
    @property
    def last_state_update_date_time(self) -> Optional[datetime]:
        """Gets the lastStateUpdateDateTime property"""
        return self.properties.get("lastStateUpdateDateTime", None)

    @odata(name="lastSyncDateTime")
    @property
    def last_sync_date_time(self) -> Optional[datetime]:
        """Gets the lastSyncDateTime property"""
        return self.properties.get("lastSyncDateTime", None)

    @odata(name="scriptError")
    @property
    def script_error(self) -> Optional[str]:
        """Gets the scriptError property"""
        return self.properties.get("scriptError", None)

    @odata(name="scriptOutput")
    @property
    def script_output(self) -> Optional[str]:
        """Gets the scriptOutput property"""
        return self.properties.get("scriptOutput", None)

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
        return "microsoft.graph.DeviceComplianceScriptDeviceState"
