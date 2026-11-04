from __future__ import annotations

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)
from office365.runtime.types.value import value


@value
class AllDevicesAssignmentTarget(DeviceAndAppManagementAssignmentTarget):
    pass
