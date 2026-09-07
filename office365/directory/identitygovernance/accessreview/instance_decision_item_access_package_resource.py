from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AccessReviewInstanceDecisionItemAccessPackageResource(ClientValue):
    accessPackageAssignmentPolicyDisplayName: str | None = None
    accessPackageAssignmentPolicyId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemAccessPackageResource"
