from __future__ import annotations

from office365.directory.applications.assignmenttype import AssignmentType
from office365.runtime.client_value import ClientValue


class PolicyAssignment(ClientValue):
    assignmentType: AssignmentType = AssignmentType.required
    displayName: str | None = None
    groupId: str | None = None
    policyId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.teamsAdministration.PolicyAssignment"
