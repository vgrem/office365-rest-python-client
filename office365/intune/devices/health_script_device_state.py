from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.common.remediation_state import RemediationState
from office365.common.run_state import RunState
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.intune.devices.management.managed.device import ManagedDevice


@version("beta")
class DeviceHealthScriptDeviceState(Entity):
    @odata(name="assignmentFilterIds")
    @property
    def assignment_filter_ids(self) -> StringCollection:
        """Gets the assignmentFilterIds property"""
        return self.properties.get("assignmentFilterIds", StringCollection())

    @odata(name="detectionState")
    @property
    def detection_state(self) -> RunState:
        """Gets the detectionState property"""
        return self.properties.get("detectionState", RunState.unknown)

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

    @odata(name="postRemediationDetectionScriptError")
    @property
    def post_remediation_detection_script_error(self) -> Optional[str]:
        """Gets the postRemediationDetectionScriptError property"""
        return self.properties.get("postRemediationDetectionScriptError", None)

    @odata(name="postRemediationDetectionScriptOutput")
    @property
    def post_remediation_detection_script_output(self) -> Optional[str]:
        """Gets the postRemediationDetectionScriptOutput property"""
        return self.properties.get("postRemediationDetectionScriptOutput", None)

    @odata(name="preRemediationDetectionScriptError")
    @property
    def pre_remediation_detection_script_error(self) -> Optional[str]:
        """Gets the preRemediationDetectionScriptError property"""
        return self.properties.get("preRemediationDetectionScriptError", None)

    @odata(name="preRemediationDetectionScriptOutput")
    @property
    def pre_remediation_detection_script_output(self) -> Optional[str]:
        """Gets the preRemediationDetectionScriptOutput property"""
        return self.properties.get("preRemediationDetectionScriptOutput", None)

    @odata(name="remediationScriptError")
    @property
    def remediation_script_error(self) -> Optional[str]:
        """Gets the remediationScriptError property"""
        return self.properties.get("remediationScriptError", None)

    @odata(name="remediationState")
    @property
    def remediation_state(self) -> Optional[RemediationState]:
        """Gets the remediationState property"""
        return self.properties.get("remediationState", None)

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
        return "microsoft.graph.DeviceHealthScriptDeviceState"
