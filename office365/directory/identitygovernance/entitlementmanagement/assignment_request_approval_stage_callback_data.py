from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.approval_stage import (
    AccessPackageApprovalStage,
)
from office365.runtime.client_value import ClientValue


class AssignmentRequestApprovalStageCallbackData(ClientValue):
    approvalStage: AccessPackageApprovalStage = field(default_factory=AccessPackageApprovalStage)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AssignmentRequestApprovalStageCallbackData"
