from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AccessReviewInstanceDecisionItemAccessPackageResource(ClientValue):
    accessPackageAssignmentPolicyDisplayName: str | None = None
    accessPackageAssignmentPolicyId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewInstanceDecisionItemAccessPackageResource"
