from __future__ import annotations

from office365.common.associated_assignment_payload_type import AssociatedAssignmentPayloadType
from office365.intune.devices.and_app_management_assignment_filter_type import DeviceAndAppManagementAssignmentFilterType
from office365.runtime.client_value import ClientValue


class PayloadByFilter(ClientValue):
    assignmentFilterType: DeviceAndAppManagementAssignmentFilterType = DeviceAndAppManagementAssignmentFilterType.none
    groupId: str | None = None
    payloadId: str | None = None
    payloadType: AssociatedAssignmentPayloadType = AssociatedAssignmentPayloadType.unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PayloadByFilter"
