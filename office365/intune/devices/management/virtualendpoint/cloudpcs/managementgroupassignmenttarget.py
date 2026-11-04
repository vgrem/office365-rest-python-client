from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class CloudPcManagementGroupAssignmentTarget(ClientValue):
    groupId: str | None = None
    servicePlanId: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.CloudPcManagementGroupAssignmentTarget"
