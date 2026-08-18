from __future__ import annotations

from dataclasses import dataclass

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)


@dataclass
class AllDevicesAssignmentTarget(DeviceAndAppManagementAssignmentTarget):
    pass
