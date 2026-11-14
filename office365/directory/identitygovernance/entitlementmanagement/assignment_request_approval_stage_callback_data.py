from __future__ import annotations

from dataclasses import field

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.approval_stage import (
    AccessPackageApprovalStage,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_request_callback_data import (
    AccessPackageAssignmentRequestCallbackData,
)


class AssignmentRequestApprovalStageCallbackData(AccessPackageAssignmentRequestCallbackData):
    approvalStage: AccessPackageApprovalStage = field(default_factory=AccessPackageApprovalStage)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AssignmentRequestApprovalStageCallbackData"
