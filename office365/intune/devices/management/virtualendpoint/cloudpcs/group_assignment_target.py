from __future__ import annotations

from office365.intune.devices.management.virtualendpoint.cloudpcs.managementassignmenttarget import (
    CloudPcManagementAssignmentTarget,
)
from office365.runtime.types.value import value


@value
class GroupAssignmentTarget(CloudPcManagementAssignmentTarget):
    groupId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupAssignmentTarget"
