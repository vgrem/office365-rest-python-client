from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.customextensionstage import (
    AccessPackageCustomExtensionStage,
)
from office365.runtime.client_value import ClientValue


class AccessPackageAssignmentRequestCallbackData(ClientValue):
    customExtensionStageInstanceDetail: str | None = None
    customExtensionStageInstanceId: str | None = None
    stage: AccessPackageCustomExtensionStage = AccessPackageCustomExtensionStage.assignmentRequestCreated
    state: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentRequestCallbackData"
