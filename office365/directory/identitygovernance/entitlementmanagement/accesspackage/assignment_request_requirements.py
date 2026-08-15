from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.question import AccessPackageQuestion
from office365.directory.identitygovernance.entitlementmanagement.schedule import EntitlementManagementSchedule
from office365.entity_collection import EntityCollection
from office365.runtime.client_value import ClientValue


@dataclass
class AccessPackageAssignmentRequestRequirements(ClientValue):
    allowCustomAssignmentSchedule: bool | None = None
    isApprovalRequiredForAdd: bool | None = None
    isApprovalRequiredForUpdate: bool | None = None
    isRequestorJustificationRequired: bool | None = None
    policyDescription: str | None = None
    policyDisplayName: str | None = None
    policyId: str | None = None
    schedule: EntitlementManagementSchedule = field(default_factory=EntitlementManagementSchedule)
    questions: EntityCollection[AccessPackageQuestion] | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentRequestRequirements"
