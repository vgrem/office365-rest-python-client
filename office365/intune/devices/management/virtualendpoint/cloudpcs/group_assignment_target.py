from __future__ import annotations

from office365.intune.devices.management.virtualendpoint.cloudpcs.managementassignmenttarget import (
    CloudPcManagementAssignmentTarget,
)


class GroupAssignmentTarget(CloudPcManagementAssignmentTarget):
    groupId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.GroupAssignmentTarget"
