from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.approval_stage import (
    AccessPackageApprovalStage,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AccessPackageAssignmentApprovalSettings(ClientValue):
    isApprovalRequiredForAdd: bool | None = None
    isApprovalRequiredForUpdate: bool | None = None
    isRequestorJustificationRequired: bool | None = None
    stages: ClientValueCollection[AccessPackageApprovalStage] = field(
        default_factory=lambda: ClientValueCollection(AccessPackageApprovalStage)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentApprovalSettings"
