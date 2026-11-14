from __future__ import annotations

from typing import Optional

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)
from office365.entity import Entity
from office365.intune.devices.health_script_run_schedule import DeviceHealthScriptRunSchedule
from office365.runtime.types.odata_property import odata, version


@version("beta")
class DeviceHealthScriptAssignment(Entity):
    @odata(name="runRemediationScript")
    @property
    def run_remediation_script(self) -> Optional[bool]:
        """Gets the runRemediationScript property"""
        return self.properties.get("runRemediationScript", None)

    @odata(name="runSchedule")
    @property
    def run_schedule(self) -> Optional[DeviceHealthScriptRunSchedule]:
        """Gets the runSchedule property"""
        return self.properties.get("runSchedule", None)

    @odata(name="target")
    @property
    def target(self) -> DeviceAndAppManagementAssignmentTarget:
        """Gets the target property"""
        return self.properties.get("target", DeviceAndAppManagementAssignmentTarget())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeviceHealthScriptAssignment"
